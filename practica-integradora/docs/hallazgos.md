# Hallazgos: Exploración visual y evidencia estadística

1. **Distribución y asimetría del salario mensual (`fig1_distribucion_salario.png`)**
   - **Evidencia:** En los 27 registros limpios, el salario mensual promedio es de **$50,004.19** (redondeado a $50,004 en el gráfico) y la mediana es de **$39,755.00** ($39,755 en el gráfico), con desviación estándar de **$48,327.92** (mínimo **$15,769.00** y máximo **$280,000.00**). La distribución está concentrada debajo de los $100,000 con un valor extremo aislado cerca de $280,000.
   - **Qué implica para negocio:** La mediana ($39,755.00) representa mejor el salario central de la plantilla, ya que la media queda jalada hacia arriba por el valor extremo.
   - **Qué NO implica:** No prueba por sí sola inequidad salarial ni explica qué variables determinan los salarios más altos.

2. **Diferencias salariales por departamento (`fig2_boxplot_salario_departamento.png`)**
   - **Evidencia:** **Operaciones** tiene la media más alta (**$76,202.50**, mediana **$41,081.50**) y la mayor dispersión (`desv_std = $100,961.48`), impulsada por un punto atípico cercano a **$280,000**; **Ventas** registra la mediana más elevada (**$55,905.00**, media **$53,927.20**), seguida de **Finanzas** (mediana **$38,629.00**, media **$42,747.00**), **RRHH** (mediana **$36,150.00**, media **$36,931.33**) y **TI** (mediana **$32,311.00**, media **$36,298.00**).
   - **Qué implica para negocio:** Conviene revisar el caso atípico en **Operaciones** y analizar las bandas salariales por área (especialmente donde la mediana es mayor, como **Ventas**).
   - **Qué NO implica:** Una diferencia visual en el boxplot no demuestra causalidad ni garantiza diferencia estadísticamente significativa sin prueba formal.

3. **Prueba de hipótesis entre dos departamentos (`Celda 8` — Welch t-test y Mann-Whitney U)**
   - **Evidencia:** Al comparar **Finanzas** (`n = 6`, media **$42,747.00**, mediana **$38,629.00**) frente a **RRHH** (`n = 6`, media **$36,931.33**, mediana **$36,150.00**), se obtuvo `Welch t-test: estadístico = 0.7831, p-value = 0.4575` y `Mann-Whitney U: estadístico = 20.0000, p-value = 0.8099`. Como ambos `p-value` son mayores a `0.05`, no se rechaza la hipótesis nula.
   - **Qué implica para negocio:** Con esta muestra no hay evidencia estadística suficiente para afirmar que exista una diferencia salarial real entre **Finanzas** y **RRHH**.
   - **Qué NO implica:** Un `p-value > 0.05` con muestras pequeñas (`n = 6` por grupo) no demuestra que los salarios poblacionales sean idénticos, debido al bajo poder estadístico.

4. **Relaciones entre variables numéricas (`fig3_heatmap_correlacion.png` y `fig5_interactiva_exp_salario.html`)**
   - **Evidencia:** En la matriz de correlación destaca la relación positiva alta entre `salario_mensual` y `es_atipico_salario` (`0.95`) y moderada con `ratio_salario_exp` (`0.61`), mientras que `anios_experiencia` muestra una correlación negativa moderada con `ratio_salario_exp` (`-0.69`) y baja correlación lineal directa con `salario_mensual` (`-0.16`). En la gráfica interactiva de `anios_experiencia` vs. `salario_mensual` por departamento se observa el punto aislado de **Operaciones** en torno a 5 años de experiencia y ~$280k, y el resto de puntos concentrados en rangos salariales menores.
   - **Qué implica para negocio:** Revisar cómo se construyeron variables derivadas (`ratio_salario_exp`, `es_atipico_salario`) y no asumir una relación lineal fuerte entre años de experiencia y salario sin segmentar por puesto o departamento.
   - **Qué NO implica:** Ninguna correlación en la matriz implica relación causal directa entre variables.

5. **Satisfacción laboral por departamento (`fig4_satisfaccion_categoria.png`)**
   - **Evidencia:** La satisfacción laboral promedio más alta aparece en **Operaciones** (cerca de `3.6–3.7`), seguida de **TI** (~`3.25`), **Finanzas** (~`2.85`) y **RRHH** (~`2.65`), mientras que **Ventas** muestra el promedio más bajo (cerca de `1.8`).
   - **Qué implica para negocio:** **Ventas** es el departamento con menor satisfacción promedio en esta muestra, por lo que convendría explorar factores de carga, metas o clima laboral en ese grupo.
   - **Qué NO implica:** No demuestra que el salario cause la satisfacción (de hecho, **Ventas** tiene mediana salarial alta y menor satisfacción promedio en la gráfica) ni reemplaza un diagnóstico cualitativo.