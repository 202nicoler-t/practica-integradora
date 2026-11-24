# Diccionario de Datos — Entregable 1

| Variable | Tipo | Descripción | Valores posibles / Rango | Notas de calidad y limpieza |
| :--- | :--- | :--- | :--- | :--- |
| `empleado_id` | `TEXT` (PK) | Identificador único del empleado | Cadena no vacía (`EMP-XXXXX` o ID original) | Se eliminan duplicados conservando el registro con mayor completitud. |
| `nombre` | `TEXT` | Nombre completo del colaborador | Texto capitalizado | Se eliminan espacios extra; nulos se etiquetan como `Sin Nombre`. |
| `edad` | `INTEGER` | Edad en años cumplidos | `18` a `75` | Valores fuera de rango o nulos se imputan con la mediana por `departamento`. |
| `rango_edad` | `TEXT` | Segmento etario derivado | `18-25`, `26-35`, `36-45`, `46+` | Variable derivada creada para análisis demográfico. |
| `departamento` | `TEXT` | Área organizacional | Texto normalizado (Title Case) | Sin espacios extra; nulos imputados con la moda del dataset. |
| `ciudad` | `TEXT` | Ciudad o sede laboral | Texto normalizado (Title Case) | Sin espacios extra; nulos imputados con la moda del dataset. |
| `anios_experiencia` | `REAL` | Años totales de experiencia laboral | `>= 0.0` | Valores negativos o nulos imputados con la mediana del `departamento`. |
| `antiguedad_empresa` | `REAL` | Años laborando en la organización | `>= 0.0` | Valores negativos o nulos imputados con la mediana del `departamento`. |
| `salario_mensual` | `REAL` | Remuneración mensual bruta | `> 0.0` | Nulos o `<= 0` imputados con la mediana por `departamento`. |
| `ratio_salario_exp` | `REAL` | Relación salario / experiencia | `salario_mensual / max(anios_experiencia, 1)` | Variable derivada para detectar brechas salariales respecto a experiencia. |
| `satisfaccion_laboral` | `REAL` | Nivel de satisfacción reportado | `1.0` a `5.0` | Valores fuera de `[1, 5]` o nulos imputados con la mediana del `departamento`. |
| `fecha_ingreso` | `TEXT` | Fecha de contratación | Formato ISO `YYYY-MM-DD` | Estandarizada con `pd.to_datetime(..., errors='coerce')`. |
| `es_atipico_salario` | `INTEGER` | Indicador binario de valor atípico | `0` (normal), `1` (atípico IQR) | Marcado mediante regla `Q1 - 1.5*IQR` y `Q3 + 1.5*IQR` sin eliminar registros. |

## Bitácora de Decisiones de Limpieza
1. **Duplicados:** Se eliminaron filas idénticas (`drop_duplicates()`) y se deduplicó por `empleado_id` conservando la fila con menos valores nulos para no perder información válida.
2. **Estandarización de categorías:** Se aplicó limpieza de espacios y formato título (`Title Case`) en `departamento` y `ciudad` para evitar fragmentación de grupos en consultas `GROUP BY`.
3. **Imputación por mediana grupal:** Para variables numéricas (`edad`, `salario_mensual`, `anios_experiencia`, `antiguedad_empresa`, `satisfaccion_laboral`) se utilizó la mediana por `departamento`, ya que es robusta frente a sesgos y valores extremos.
4. **Tratamiento de atípicos:** En lugar de borrar salarios altos/bajos reales, se creó la bandera `es_atipico_salario` mediante rango intercuartílico (IQR) para mantener trazabilidad en RR. HH.
5. **Variables derivadas:** Se incorporaron `rango_edad` y `ratio_salario_exp` para enriquecer la segmentación exploratoria y el modelado posterior.
