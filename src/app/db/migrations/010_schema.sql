CREATE TABLE format_type (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(30) NOT NULL UNIQUE,
  description VARCHAR(120)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE product (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  dosage_per_m2 DECIMAL(18,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE culture (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(60) NOT NULL UNIQUE,
  product_id INT NOT NULL,
  format_id INT NOT NULL,
  street_size_m DECIMAL(18,4) NOT NULL,
  CONSTRAINT fk_culture_product
    FOREIGN KEY (product_id) REFERENCES product(id)
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_culture_format
    FOREIGN KEY (format_id) REFERENCES format_type(id)
      ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE system_param (
  `key` VARCHAR(80) PRIMARY KEY,
  value_str VARCHAR(4000),
  value_num DECIMAL(18,4)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE planting_calculation (
  id INT AUTO_INCREMENT PRIMARY KEY,
  culture_id INT NOT NULL,
  product_id INT NOT NULL,
  total_area_m2 DECIMAL(18,4) NOT NULL,     -- área total informada
  planting_area_m2 DECIMAL(18,4) NOT NULL,  -- área útil calculada
  number_of_streets INT NOT NULL,           -- ruas calculadas
  product_qty DECIMAL(18,4) NOT NULL,       -- quantidade do insumo
  input_params JSON NULL,                   -- parâmetros de entrada (ex.: largura/altura, formato)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_pc_culture
    FOREIGN KEY (culture_id) REFERENCES culture(id)
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pc_product
    FOREIGN KEY (product_id) REFERENCES product(id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

  INDEX ix_pc_culture (culture_id),
  INDEX ix_pc_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE iot_reading (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    humidity DECIMAL(5,2) NOT NULL,
    ph DECIMAL(5,2) NOT NULL,
    phosphorus TINYINT(1) NOT NULL,
    potassium TINYINT(1) NOT NULL,
    pump_on TINYINT(1) NOT NULL,
    CONSTRAINT chk_ph CHECK (ph >= 0 AND ph <= 14),
    CONSTRAINT chk_humidity CHECK (humidity >= 0 AND humidity <= 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

