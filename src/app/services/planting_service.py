# app/services/planting_service.py
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, List, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.culture_model import Culture
from app.db.models.product_model import Product
from app.db.models.format_type_model import FormatType
from app.db.models.system_param_model import SystemParam
from app.db.models.planting_calculation_model import PlantingCalculation as PC


class PlantingService:
    SPACE_BETWEEN_STREETS_KEY = "SPACE_BETWEEN_STREETS_M"

    # -------------------------
    # 1) Listar culturas (JOIN)
    # -------------------------
    @staticmethod
    def get_cultures(session: Session) -> List[Dict[str, Any]]:
        stmt = (
            select(
                Culture.id,
                Culture.name,
                Product.name.label("product_name"),
                FormatType.code.label("format_type_name"),
                Culture.street_size_m,
            )
            .join(Product, Product.id == Culture.product_id)
            .join(FormatType, FormatType.id == Culture.format_id)
            .order_by(Culture.name)
        )
        rows = session.execute(stmt).all()
        return [
            {
                "id": r.id,
                "name": r.name,
                "product_name": r.product_name,
                "format_type_name": r.format_type_name,
                "street_size_m": str(r.street_size_m),
            }
            for r in rows
        ]

    # --------------------------------------------------------------------
    # 2) Calcular área de plantio e registrar em planting_calculation (INSERT)
    # --------------------------------------------------------------------
    @staticmethod
    def calc_and_register(
        session: Session,
        culture: int | str,          # pode ser ID (int) ou NAME (str)
        total_area_m2: Decimal | float | int,
    ) -> Dict[str, Any]:
        # Normaliza área como Decimal
        total_area = Decimal(str(total_area_m2))

        # Carrega cultura + produto + formato
        q = (
            select(
                Culture.id,
                Culture.name,
                Culture.street_size_m,
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.dosage_per_m2,
                FormatType.id.label("format_id"),
                FormatType.code.label("format_code"),
            )
            .join(Product, Product.id == Culture.product_id)
            .join(FormatType, FormatType.id == Culture.format_id)
        )
        if isinstance(culture, int):
            q = q.where(Culture.id == culture)
        else:
            q = q.where(Culture.name == culture)

        row = session.execute(q).first()
        if not row:
            raise ValueError("Cultura não encontrada.")

        # Pega parâmetro global SPACE_BETWEEN_STREETS_M
        space_between = session.get(SystemParam, PlantingService.SPACE_BETWEEN_STREETS_KEY)
        if not space_between or space_between.value_num is None:
            raise ValueError("Parâmetro global 'SPACE_BETWEEN_STREETS_M' não configurado.")

        street_size = Decimal(str(row.street_size_m))
        space_between_streets = Decimal(str(space_between.value_num))
        format_code = row.format_code  # 'retangulo' | 'triangulo'
        dosage_per_m2 = Decimal(str(row.dosage_per_m2))

        # --- Cálculo da área disponível, replicando a sua lógica do script ---
        planting_area, number_of_streets = PlantingService._calc_area_available(
            total_area,
            format_code,
            street_size,
            space_between_streets,
        )

        # Quantidade de produto
        product_qty = (dosage_per_m2 * planting_area).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        # Persiste em planting_calculation
        new_row = PC(
            culture_id=row.id,
            product_id=row.product_id,
            total_area_m2=planting_area + (number_of_streets * street_size),  # opcional: guardar exatamente total_area recebido
            planting_area_m2=planting_area,
            number_of_streets=number_of_streets,
            product_qty=product_qty,
            input_params={
                "format": format_code,
                "street_size_m": str(street_size),
                "space_between_streets_m": str(space_between_streets),
                "total_area_input_m2": str(total_area),
            },
        )
        session.add(new_row)
        session.commit()
        session.refresh(new_row)

        return {
            "id": new_row.id,
            "culture_id": row.id,
            "culture_name": row.name,
            "product_id": row.product_id,
            "product_name": row.product_name,
            "format_type_id": row.format_id,
            "format_type_code": row.format_code,
            "total_area_m2": str(total_area),
            "planting_area_m2": str(new_row.planting_area_m2),
            "number_of_streets": new_row.number_of_streets,
            "product_qty": str(new_row.product_qty),
            "created_at": str(new_row.created_at),
        }

    # -----------------------------
    # Função privada de cálculo
    # (mesma lógica do seu script)
    # -----------------------------
    @staticmethod
    def _calc_area_available(
        area: Decimal,
        figure: str,
        street_size: Decimal,
        space_between_streets: Decimal,
    ) -> tuple[Decimal, int]:
        """
        Retorna (planting_area, number_of_streets)
        Lógica espelhada do seu script:
          - retangulo:
               totalStreetSize = street_size + space_between_streets
               streetsQtd = floor(area / totalStreetSize)
               areaOccupiedByStreets = streetsQtd * street_size
               plantingArea = area - areaOccupiedByStreets
          - triangulo:
               base = sqrt(2 * area)
               height = base / 2
               totalArea = (base * height) / 2
               totalStreetSize = street_size + space_between_streets
               streetsQtd = floor(height / totalStreetSize)
               areaAvailable = totalArea - (streetsQtd * street_size * base / totalArea)
        """
        from math import floor, sqrt

        if figure == "retangulo":
            total_street_size = street_size + space_between_streets
            streets_qtd = int(floor(area / total_street_size))
            area_occupied = Decimal(streets_qtd) * street_size
            planting_area = area - area_occupied
            return (planting_area, streets_qtd)

        elif figure == "triangulo":
            # espelha a matemática do script original
            base = Decimal(str(sqrt(2 * float(area))))
            height = base / Decimal("2")
            total_area = (base * height) / Decimal("2")
            total_street_size = street_size + space_between_streets
            streets_qtd = int(floor(float(height / total_street_size)))
            # Nota: fórmula do script tem dimensões peculiares; replicamos:
            area_available = total_area - (Decimal(streets_qtd) * street_size * base / total_area)
            return (area_available, streets_qtd)

        else:
            raise ValueError(f"Figura desconhecida: {figure}")

    @staticmethod
    def get_calcs(
            session: Session,
            limit: int | None = None,
            offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Lista registros de planting_calculation, juntando nomes de cultura e produto.
        Ordena por created_at desc. Suporta paginação via limit/offset.
        """
        stmt = (
            select(
                PC.id,
                PC.created_at,
                PC.total_area_m2,
                PC.planting_area_m2,
                PC.number_of_streets,
                PC.product_qty,
                PC.input_params,
                Culture.id.label("culture_id"),
                Culture.name.label("culture_name"),
                Product.id.label("product_id"),
                Product.name.label("product_name"),
            )
            .join(Culture, Culture.id == PC.culture_id)
            .join(Product, Product.id == PC.product_id)
            .order_by(PC.created_at.desc(), PC.id.desc())
        )

        if limit is not None:
            stmt = stmt.limit(limit).offset(offset)

        rows = session.execute(stmt).all()

        def _s(v):
            # normaliza Decimals/None para string quando numérico
            return str(v) if v is not None else None

        return [
            {
                "id": r.id,
                "created_at": str(r.created_at),
                "culture_id": r.culture_id,
                "culture_name": r.culture_name,
                "product_id": r.product_id,
                "product_name": r.product_name,
                "total_area_m2": _s(r.total_area_m2),
                "planting_area_m2": _s(r.planting_area_m2),
                "number_of_streets": r.number_of_streets,
                "product_qty": _s(r.product_qty),
                "input_params": r.input_params,
            }
            for r in rows
        ]
