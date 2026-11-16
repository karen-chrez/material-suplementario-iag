# Prompts IDEAR para los cinco problemas

Material suplementario S1b. Condición experimental: IDEAR (comparar contra la condición zero-shot «Resuelve este problema.»).

## Protocolo de aplicación (idéntico al zero-shot salvo el texto del prompt)

1. Usar el mismo modelo y nivel de razonamiento en ambas condiciones (zero-shot e IDEAR) y correr las dos el mismo día. ChatGPT: GPT-5.6 SOL Alta, cuenta Plus (si sigue disponible). Gemini: 3.6 Thinking ya fue retirado; usar 4 Hydrogen Thinking, cuenta educativa, en ambas condiciones. Registrar el nombre exacto del modelo, la fecha y la hora.
2. Abrir una conversación nueva por problema. Desactivar memoria / instrucciones personalizadas (ChatGPT: Memoria e Instrucciones personalizadas; Gemini: Información guardada y actividad de apps).
3. Adjuntar la MISMA imagen del enunciado usada en el zero-shot (EJERCICIO10.PNG, EJERCICIO1.PNG, EJERCICIO6.PNG, EJERCICIO5.PNG, EJERCICIO2.PNG).
4. Pegar el prompt completo en un solo mensaje. No hacer preguntas de seguimiento.
5. Conservar la primera respuesta completa; no regenerar. Si se hacen repeticiones, abrir una conversación nueva para cada una y conservarlas todas.
6. Guardar la conversación con Imprimir → Guardar como PDF desde el navegador (debe verse prompt, fecha y respuesta) y descargar los archivos .m que el sistema entregue.
7. Obligatorio para Gemini y recomendado para ChatGPT: repetir el zero-shot («Resuelve este problema.» + la misma imagen) el mismo día que IDEAR, con el mismo modelo. Las respuestas zero-shot originales (agosto–septiembre de 2026) se conservan como corrida original y no se reemplazan.

---

## Problema a) Ecuaciones diferenciales ordinarias (EJERCICIO10.PNG)

```
[Identidad] Eres profesor de Matemáticas Avanzadas en un posgrado de ingeniería en control automático.

[Destinatario] Escribe para un estudiante de primer semestre de maestría que ya cursó ecuaciones diferenciales ordinarias en licenciatura. Justifica cada paso que no sea una operación algebraica elemental.

[Estructura]
- Organiza la respuesta por inciso, con el mismo orden y nombre que en el enunciado.
- Escribe una ecuación por línea.
- Responde exactamente lo que pide el enunciado.
- Termina con una tabla resumen con el resultado de cada inciso.
- Incluye al final un bloque de código MATLAB que verifique los resultados, ejecutable sin modificaciones, y reporta el valor de todos los parámetros numéricos que utilice.

[Acción] Resuelve el problema de la imagen adjunta.

[Referencia] Usa la notación de operadores D = d/dx y el método de coeficientes indeterminados (enfoque del anulador) como en Zill, Ecuaciones diferenciales con aplicaciones de modelado. Si algún término de la forma propuesta coincide con la solución homogénea, indícalo explícitamente.
```

## Problema b) Transformada de Laplace (EJERCICIO1.PNG)

```
[Identidad] Eres profesor de Matemáticas Avanzadas en un posgrado de ingeniería en control automático.

[Destinatario] Escribe para un estudiante de primer semestre de maestría que ya cursó ecuaciones diferenciales y conoce la transformada de Laplace. Justifica cada paso que no sea una operación algebraica elemental.

[Estructura]
- Organiza la respuesta por inciso, con el mismo orden y nombre que en el enunciado.
- Escribe una ecuación por línea.
- Responde exactamente lo que pide el enunciado.
- Termina con una tabla resumen con el resultado de cada inciso.
- Incluye al final un bloque de código MATLAB que verifique los resultados, ejecutable sin modificaciones, y reporta el valor de todos los parámetros numéricos que utilice (intervalo de tiempo, paso, condiciones iniciales y matrices empleadas).

[Acción] Resuelve el problema de la imagen adjunta.

[Referencia] Las condiciones iniciales están definidas en t = 0⁻ y la entrada u(t) es un escalón unitario aplicado en t = 0. Usa la transformada unilateral de Laplace con la convención de Ogata, Ingeniería de control moderna.
```

## Problema c) Transformada Z (EJERCICIO6.PNG)

```
[Identidad] Eres profesor de Matemáticas Avanzadas en un posgrado de ingeniería en control automático.

[Destinatario] Escribe para un estudiante de primer semestre de maestría que ya cursó control clásico en tiempo continuo pero no sistemas en tiempo discreto. Justifica cada paso que no sea una operación algebraica elemental.

[Estructura]
- Organiza la respuesta por inciso, con el mismo orden y nombre que en el enunciado.
- Escribe una ecuación por línea.
- Responde exactamente lo que pide el enunciado.
- Termina con una tabla resumen con el resultado de cada inciso.
- Incluye al final un bloque de código MATLAB que verifique los resultados, ejecutable sin modificaciones, y reporta el valor de todos los parámetros numéricos que utilice.

[Acción] Resuelve el problema de la imagen adjunta.

[Referencia] Usa retenedor de orden cero, la notación de Ogata, Sistemas de control en tiempo discreto, y el criterio de asentamiento del 2 %. Los valores de sobrepaso y tiempo de asentamiento que reportes deben corresponder a la respuesta al escalón del sistema en lazo cerrado, no sólo a una aproximación de segundo orden; si usas una aproximación, indícalo.
```

## Problema d) Espacio de estado (EJERCICIO5.PNG)

```
[Identidad] Eres profesor de Matemáticas Avanzadas en un posgrado de ingeniería en control automático.

[Destinatario] Escribe para un estudiante de primer semestre de maestría que ya cursó control clásico y álgebra lineal, pero no control en espacio de estado. Justifica cada paso que no sea una operación algebraica elemental.

[Estructura]
- Organiza la respuesta por inciso, con el mismo orden y nombre que en el enunciado.
- Escribe una ecuación por línea.
- Responde exactamente lo que pide el enunciado.
- Termina con una tabla resumen con el resultado de cada inciso.
- Incluye al final un bloque de código MATLAB que verifique los resultados, ejecutable sin modificaciones, y reporta el valor de todos los parámetros numéricos que utilice (paso de integración, intervalo de tiempo, referencia y condiciones iniciales del sistema y del estimador).

[Acción] Resuelve el problema de la imagen adjunta.

[Referencia] Usa la notación de Ogata, Ingeniería de control moderna: u = r − K x̂ y estimador de orden completo x̂' = A x̂ + B u + L (y − C x̂). Usa la ley de control exactamente como está planteada en el enunciado.
```

## Problema e) Respuesta en frecuencia (EJERCICIO2.PNG)

```
[Identidad] Eres profesor de Matemáticas Avanzadas en un posgrado de ingeniería en control automático.

[Destinatario] Escribe para un estudiante de primer semestre de maestría que ya cursó control clásico en tiempo continuo. Justifica cada paso que no sea una operación algebraica elemental.

[Estructura]
- Organiza la respuesta por inciso, con el mismo orden y nombre que en el enunciado.
- Escribe una ecuación por línea.
- Responde exactamente lo que pide el enunciado.
- Termina con una tabla resumen con el resultado de cada inciso, incluyendo la frecuencia asociada a cada ganancia.
- Incluye al final un bloque de código MATLAB que verifique los resultados, ejecutable sin modificaciones, y reporta el valor de todos los parámetros numéricos que utilice.

[Acción] Resuelve el problema de la imagen adjunta.

[Referencia] Usa la notación de Ogata, Ingeniería de control moderna: margen de fase, margen de ganancia, máximo módulo de lazo cerrado Mr en dB y carta de Nichols. Expresa el margen de ganancia como cociente (no en dB) salvo que el enunciado indique otra cosa.
```

---

## Qué registrar por cada ejecución

| Campo | Ejemplo |
|---|---|
| Problema / condición / sistema | b / IDEAR / Gemini |
| Modelo y nivel | Gemini 3.6 Thinking |
| Fecha y hora | 2026-11-12 10:15 (UTC−6) |
| Número de ejecución | 1 de 1 |
| Archivo de la respuesta | b_IDEAR_Gemini_1.pdf |
| Archivos de código entregados | b_IDEAR_Gemini_1.m |
| ¿Se ejecutó sin error? | sí / no |
| Exactitud del resultado | correcto / incorrecto (por inciso) |
| Validez del procedimiento | válido / con errores (por inciso) |
