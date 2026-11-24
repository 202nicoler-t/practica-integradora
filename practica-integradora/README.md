# Práctica Integradora — Analítica de Datos (Entregable 1)

## Estructura del Proyecto
```text
practica-integradora-gab2402/
├── data/          # Coloca aquí empleados_analitica.csv; aquí se genera empleados_limpio.db
├── notebooks/     # 01_limpieza_y_bd.ipynb y pipeline_entregable_1.py
├── sql/           # schema.sql con definición de tablas e índices SQLite
├── models/        # Modelos serializados (Entregable 3)
├── app/           # Aplicación interactiva (Entregable 4)
├── docs/          # diccionario_datos.md y bitácora de limpieza
└── README.md
```

## Cómo ejecutar (reproducible)
1. Asegúrate de tener tu archivo `empleados_analitica.csv` dentro de la carpeta `data/`.
2. Instala dependencias básicas si no las tienes:
   ```bash
   pip install pandas numpy jupyter
   ```
3. Ejecuta el pipeline desde la raíz del proyecto:
   ```bash
   python notebooks/pipeline_entregable_1.py
   ```
   O abre y ejecuta todas las celdas de `notebooks/01_limpieza_y_bd.ipynb`.
4. Esto creará/actualizará `data/empleados_limpio.db` aplicando `sql/schema.sql` y mostrará las consultas de verificación en consola.
