from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd


def resolve_base_dir() -> Path:
    """Detecta la raíz del repositorio buscando la carpeta 'data'."""
    candidates = [Path.cwd(), Path.cwd().parent]
    if "__file__" in globals():
        here = Path(__file__).resolve().parent
        candidates = [here, here.parent, here.parent.parent] + candidates

    for candidate in candidates:
        if (candidate / "data" / "empleados_analitica.csv").exists():
            return candidate
    raise FileNotFoundError(
        "No se encontró 'data/empleados_analitica.csv'. Coloca tu CSV dentro de 'data/' y vuelve a ejecutar."
    )


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas a snake_case sin acentos ni espacios."""
    replacements = str.maketrans({
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u", "Ñ": "n",
    })
    df = df.copy()
    df.columns = [
        col.strip().translate(replacements).lower().replace(" ", "_")
        for col in df.columns
    ]
    return df


def run_pipeline() -> None:
    base_dir = resolve_base_dir()
    csv_path = base_dir / "data" / "empleados_analitica.csv"
    db_path = base_dir / "data" / "empleados_limpio.db"
    schema_path = base_dir / "sql" / "schema.sql"

    # 1. Exploración inicial
    df_raw = pd.read_csv(csv_path)
    print(f"Filas iniciales: {len(df_raw)} | Columnas iniciales: {len(df_raw.columns)}")
    print("Nulos iniciales por columna:")
    print(df_raw.isna().sum()[df_raw.isna().sum() > 0])
    print(f"Duplicados exactos iniciales: {df_raw.duplicated().sum()}\n")

    df = clean_column_names(df_raw)

    # Aliases comunes por si el CSV usa nombres ligeramente distintos
    alias_map = {
        "id_empleado": "empleado_id",
        "id": "empleado_id",
        "experiencia": "anios_experiencia",
        "anios_exp": "anios_experiencia",
        "antiguedad": "antiguedad_empresa",
        "salario": "salario_mensual",
        "sueldo": "salario_mensual",
        "satisfaccion": "satisfaccion_laboral",
    }
    for src, dst in alias_map.items():
        if src in df.columns and dst not in df.columns:
            df[dst] = df[src]

    # 2. Eliminación de duplicados exactos y por ID (conservando el registro más completo)
    df = df.drop_duplicates().copy()
    if "empleado_id" in df.columns:
        df["empleado_id"] = df["empleado_id"].astype(str).str.strip()
        df = df[df["empleado_id"].notna() & (df["empleado_id"] != "") & (df["empleado_id"] != "nan")]
        df["_non_null_count"] = df.notna().sum(axis=1)
        df = (
            df.sort_values(by=["empleado_id", "_non_null_count"], ascending=[True, False])
            .drop_duplicates(subset=["empleado_id"], keep="first")
            .drop(columns=["_non_null_count"])
        )
    else:
        df.insert(0, "empleado_id", [f"EMP-{i+1:05d}" for i in range(len(df))])

    # 3. Normalización de texto y categorías
    if "nombre" in df.columns:
        df["nombre"] = df["nombre"].astype(str).str.strip().str.title()
        df.loc[df["nombre"].isin(["", "Nan", "None"]), "nombre"] = "Sin Nombre"
    else:
        df["nombre"] = "Sin Nombre"

    for col, default_val in [("departamento", "General"), ("ciudad", "No Especificada")]:
        if col in df.columns:
            cleaned = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.title()
            )
            cleaned = cleaned.where(~cleaned.isin(["", "Nan", "None", "Null"]), np.nan)
            mode_val = cleaned.mode(dropna=True)
            fill_val = mode_val.iloc[0] if not mode_val.empty else default_val
            df[col] = cleaned.fillna(fill_val)
        else:
            df[col] = default_val

    # 4. Normalización numérica, rangos e imputación justificada
    if "edad" in df.columns:
        df["edad"] = pd.to_numeric(df["edad"], errors="coerce")
        df.loc[(df["edad"] < 18) | (df["edad"] > 75), "edad"] = np.nan
        med_edad = df["edad"].median()
        df["edad"] = (
            df.groupby("departamento")["edad"]
            .transform(lambda s: s.fillna(s.median()))
            .fillna(med_edad if pd.notna(med_edad) else 30)
            .round()
            .astype(int)
        )
    else:
        df["edad"] = 30

    for col, default_val in [("anios_experiencia", 0.0), ("antiguedad_empresa", 0.0)]:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce")
            s = s.where(s >= 0, np.nan)
            med_val = s.median()
            df[col] = (
                s.groupby(df["departamento"])
                .transform(lambda grp: grp.fillna(grp.median()))
                .fillna(med_val if pd.notna(med_val) else default_val)
                .round(1)
            )
        else:
            df[col] = default_val

    if "salario_mensual" in df.columns:
        sal = pd.to_numeric(df["salario_mensual"], errors="coerce")
        sal = sal.where(sal > 0, np.nan)
        med_sal = sal.median()
        df["salario_mensual"] = (
            sal.groupby(df["departamento"])
            .transform(lambda grp: grp.fillna(grp.median()))
            .fillna(med_sal if pd.notna(med_sal) else 15000.0)
            .round(2)
        )
    else:
        df["salario_mensual"] = 15000.0

    if "satisfaccion_laboral" in df.columns:
        sat = pd.to_numeric(df["satisfaccion_laboral"], errors="coerce")
        sat = sat.where((sat >= 1) & (sat <= 5), np.nan)
        med_sat = sat.median()
        df["satisfaccion_laboral"] = (
            sat.groupby(df["departamento"])
            .transform(lambda grp: grp.fillna(grp.median()))
            .fillna(med_sat if pd.notna(med_sat) else 3.0)
            .round(1)
        )
    else:
        df["satisfaccion_laboral"] = 3.0

    if "fecha_ingreso" in df.columns:
        fechas = pd.to_datetime(df["fecha_ingreso"], errors="coerce")
        df["fecha_ingreso"] = fechas.dt.strftime("%Y-%m-%d").fillna("")
    else:
        df["fecha_ingreso"] = ""

    # 5. Marcado de valores atípicos en salario (criterio IQR sin borrar registros)
    q1 = df["salario_mensual"].quantile(0.25)
    q3 = df["salario_mensual"].quantile(0.75)
    iqr = q3 - q1
    lim_inf = max(0.0, q1 - 1.5 * iqr)
    lim_sup = q3 + 1.5 * iqr
    df["es_atipico_salario"] = (
        (df["salario_mensual"] < lim_inf) | (df["salario_mensual"] > lim_sup)
    ).astype(int)

    # 6. Variables derivadas
    df["rango_edad"] = pd.cut(
        df["edad"],
        bins=[17, 25, 35, 45, 100],
        labels=["18-25", "26-35", "36-45", "46+"],
    ).astype(str)

    df["ratio_salario_exp"] = (
        df["salario_mensual"] / np.maximum(df["anios_experiencia"], 1.0)
    ).round(2)

    # 7. Persistencia en SQLite
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_path.read_text(encoding="utf-8"))
        cols_tabla = [
            row[1] for row in conn.execute("PRAGMA table_info(empleados)").fetchall()
        ]
        df_to_load = df[cols_tabla]
        df_to_load.to_sql("empleados", conn, if_exists="append", index=False)
        conn.commit()

        # 8. Consultas de comprobación
        total = pd.read_sql("SELECT COUNT(*) AS total FROM empleados", conn).iloc[0, 0]
        resumen_dept = pd.read_sql(
            """
            SELECT
                departamento,
                COUNT(*) AS empleados,
                ROUND(AVG(salario_mensual), 2) AS salario_promedio,
                ROUND(AVG(satisfaccion_laboral), 2) AS satisfaccion_promedio,
                SUM(es_atipico_salario) AS atipicos_salario
            FROM empleados
            GROUP BY departamento
            ORDER BY salario_promedio DESC
            """,
            conn,
        )
        resumen_ciudad = pd.read_sql(
            """
            SELECT
                ciudad,
                COUNT(*) AS empleados,
                ROUND(AVG(salario_mensual), 2) AS salario_promedio
            FROM empleados
            GROUP BY ciudad
            ORDER BY empleados DESC
            """,
            conn,
        )
    finally:
        conn.close()

    print(f"Base generada en: {db_path}")
    print(f"Total de registros limpios insertados: {total}\n")
    print("--- Resumen por departamento ---")
    print(resumen_dept.to_string(index=False))
    print("\n--- Resumen por ciudad ---")
    print(resumen_ciudad.to_string(index=False))


if __name__ == "__main__":
    run_pipeline()
