import os
import requests


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather_by_city(city: str) -> dict:
        city = (city or "").strip()
        if not city:
            return {
                "status": "error",
                "detail": "Cidade não informada."
            }

        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if not api_key:
            return {
                "status": "error",
                "detail": "API key do OpenWeather não configurada (OPENWEATHER_API_KEY)."
            }

        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "lang": "pt_br",
        }

        try:
            resp = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
        except requests.RequestException as e:
            return {
                "status": "error",
                "detail": f"Erro de conexão com serviço de clima: {e}"
            }

        if resp.status_code != 200:
            try:
                payload = resp.json()
                msg = payload.get("message", "Erro ao consultar clima.")
            except Exception:
                msg = f"Erro HTTP {resp.status_code} ao consultar clima."
            return {
                "status": "error",
                "detail": msg
            }

        payload = resp.json()

        # valida estrutura mínima
        if "main" not in payload or "weather" not in payload:
            return {
                "status": "error",
                "detail": "Resposta inesperada da API de clima."
            }

        data = {
            "city": payload.get("name"),
            "country": payload.get("sys", {}).get("country"),
            "temperature": payload["main"].get("temp"),
            "humidity": payload["main"].get("humidity"),
            "pressure": payload["main"].get("pressure"),
            "wind_speed": payload.get("wind", {}).get("speed"),
            "lat": payload.get("coord", {}).get("lat"),
            "lon": payload.get("coord", {}).get("lon"),
            "description": payload["weather"][0].get("description") if payload["weather"] else None,
        }

        return {
            "status": "success",
            "data": data
        }
