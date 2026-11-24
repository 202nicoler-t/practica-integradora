PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS empleados;

CREATE TABLE empleados (
    empleado_id TEXT PRIMARY KEY,
    nombre TEXT,
    edad INTEGER CHECK (edad BETWEEN 18 AND 75),
    rango_edad TEXT,
    departamento TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    anios_experiencia REAL CHECK (anios_experiencia >= 0),
    antiguedad_empresa REAL CHECK (antiguedad_empresa >= 0),
    salario_mensual REAL CHECK (salario_mensual > 0),
    ratio_salario_exp REAL,
    satisfaccion_laboral REAL CHECK (satisfaccion_laboral BETWEEN 1 AND 5),
    fecha_ingreso TEXT,
    es_atipico_salario INTEGER DEFAULT 0
);

CREATE INDEX idx_empleados_departamento ON empleados(departamento);
CREATE INDEX idx_empleados_ciudad ON empleados(ciudad);
CREATE INDEX idx_empleados_dept_ciudad ON empleados(departamento, ciudad);
