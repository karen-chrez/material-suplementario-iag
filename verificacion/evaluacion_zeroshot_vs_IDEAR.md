# Evaluación de respuestas: zero-shot vs IDEAR

Material suplementario S4. Evaluación independiente de 20 respuestas (5 problemas × 2 condiciones × 2 sistemas) más la corrida original de Gemini 3.6 Thinking como referencia histórica.

## Corridas evaluadas

| Sistema | Condición | Modelo (según el documento) | Fecha | Estado |
|---|---|---|---|---|
| ChatGPT | Zero-shot | GPT-5.6 Sol, razonamiento alto | 3–31 ago 2026 (conversaciones originales) | Válida |
| ChatGPT | IDEAR | GPT-5.6 Sol, razonamiento alto | 12–15 nov 2026 | Válida: una conversación nueva por problema |
| Gemini | Zero-shot | Hydrogen Thinking, esfuerzo 1.00 | 14–15 nov 2026 | Válida |
| Gemini | IDEAR | Hydrogen Thinking, esfuerzo 1.00 | 14–15 nov 2026 | Válida |
| Gemini (original) | Zero-shot | 3.6 Thinking (retirado) | 3 ago – 7 sep 2026 | Referencia histórica |

Las 20 respuestas se obtuvieron en 20 conversaciones independientes. La versión enviada del artículo indicaba que las respuestas originales se obtuvieron con IDEAR; en realidad se obtuvieron con el prompt zero-shot, y la condición IDEAR se añadió en noviembre de 2026. En ChatGPT, zero-shot (agosto) e IDEAR (noviembre) se ejecutaron en meses distintos con el mismo modelo nominal; no puede descartarse una actualización del proveedor entre ambas fechas.

Los documentos de ChatGPT IDEAR de los problemas b) y e) se regeneraron para corregir los metadatos; su redacción cambió, pero se comprobó que todos los resultados, matrices, condiciones iniciales y ganancias coinciden con la versión evaluada.

Nota: los 20 PDFs son documentos que generó cada modelo a petición del autor al final de la conversación, no impresiones de la conversación. Esa petición adicional debe declararse en la metodología, y las conversaciones originales deben archivarse aparte.

## Criterios

- **Exactitud del resultado (R):** cada resultado solicitado coincide con la referencia verificada (simbólica: residuo nulo; numérica: error relativo < 10⁻³ en ganancias y frecuencias, < 10⁻⁸ en simulaciones).
- **Validez del procedimiento (P):** el desarrollo no contiene errores de razonamiento ni afirmaciones falsas sobre su propio resultado.
- **Código (C):** matrices, condiciones iniciales y parámetros del código reproducen el resultado. Se verificó reimplementando en Python (python-control/SciPy); **falta ejecutar los .m originales en MATLAB**.

✓ = correcto · ◐ = correcto con observación · ✗ = incorrecto

## Resultados

| Problema | ChatGPT ZS | ChatGPT IDEAR | Gemini ZS (Hydrogen) | Gemini IDEAR (Hydrogen) | Gemini ZS original (3.6) |
|---|---|---|---|---|---|
| a) EDO | ✓ forma + coeficientes (no pedidos) | ✓ forma + coeficientes | ✓ forma | ✓ forma + coeficientes | ✓ forma |
| b) Laplace | ✓ analítico; código ✓ (x₀=[1;3]) | ✓ analítico; código ✓ (x₀=[1;3]) | ✓ analítico; código ✓ (x₀ = obsv\[1;3]) | ✓ analítico; código ✓ (forma canónica observable, x₀=[1;5]) | ✓ analítico; **código ✗** (x₀ de otra realización) |
| c) Z | ◐ Kz=0.0038751, Ka=0.01589735 | ◐ K=0.004, Ka=0.0155 | ✓ compensadores de adelanto | ◐ K=0.0038, Ka=0.015432 | ◐ Kd=0.0035, Ka=0.0154 |
| d) Estado | ✓ advierte y(∞)=−0.25 | ✓ advierte y(∞)=−0.25 | ◐ no advierte y(∞)=−0.25 | ✓ advierte y(∞)=−0.25 | ◐ no advierte y(∞)=−0.25 |
| e) Frecuencia | ✓ | ✓ | ✓ | ✓ | ✓ |

### Detalle problema c) Transformada Z

Especificaciones: Mp ≤ 10 %, ts(2 %) ≤ 5 s, tr mínimo, ess = 0.

| Respuesta | Controlador | Mp en muestras | Mp continuo (entre muestras) | ts muestras | Lo que reporta la respuesta |
|---|---|---|---|---|---|
| ChatGPT ZS | C(z)=0.0038751 | 8.13 % | **11.20 %** | 4 s | 8.125 %, 4 s ✓ (en muestras) |
| ChatGPT IDEAR | C(z)=0.004 | 9.99 % | **12.63 %** | 4 s | 9.986 %, 4 s ✓ (en muestras) |
| Gemini IDEAR | C(z)=0.0038 | 7.62 % | **10.33 %** | 4 s | 7.62 %, 4 s ✓ (en muestras) |
| Gemini ZS | C(z)=0.0045(z−0.006738)/(z+0.20) | 0.00 % | 0 % | 2 s | 0 %, 2 s, «también entre muestras» ✓ |
| Gemini 3.6 (ago) | C(z)=0.0035 | 6.55 % | — | 5 s | 7.2 %, 4.3 s ✗ (aproximación de 2.º orden) |

| Respuesta | Controlador analógico | Mp | ts | tr | Lo que reporta |
|---|---|---|---|---|---|
| ChatGPT ZS | 0.01589735 | 10.00 % | 1.401 s | 0.433 s | 10 %, 1.40 s, 0.433 s ✓ |
| ChatGPT IDEAR | 0.0155 | 9.56 % | 1.423 s | 0.443 s | 9.555 %, 1.423 s, 0.4435 s ✓ |
| Gemini IDEAR | 0.015432 | 9.48 % | 1.426 s | 0.445 s | 9.48 %, **1.39 s**, 0.45 s ◐ |
| Gemini ZS | 0.2104(s+5)/(s+20) | 6.81 % | 0.390 s | 0.129 s | 6.78 %, 0.40 s, 0.12 s ✓ |
| Gemini 3.6 (ago) | 0.0154 | 9.44 % | 1.43 s | — | 9.5 %, **1.6 s** ◐ |

Observación: todos los controladores discretos proporcionales cumplen Mp ≤ 10 % solo en los instantes de muestreo; la salida continua de la planta lo excede entre muestras. Ninguna de esas respuestas lo menciona. Esto también afecta al resultado que el artículo presenta como referencia (Kz = 0.0038751).

### Detalle problema d) Simulación de Euler

| Respuesta | h | x(0) | x̂(0) |
|---|---|---|---|
| ChatGPT ZS | 0.001 s (8 s) | [1; −1] | [0; 1] |
| ChatGPT IDEAR | 0.001 s (10 s) | [1; −1] | [0; 0] |
| Gemini ZS | 0.001 s | [2; −1] | [0; 0] |
| Gemini IDEAR | 0.001 s | [2; −1] | [0; 0] |

Ninguna respuesta estudia la sensibilidad al paso de integración.

## Hallazgos

1. **Exactitud:** en los cinco problemas, IDEAR no cambió la exactitud de los resultados analíticos en ninguno de los dos sistemas. Las cuatro corridas del modelo actual resolvieron correctamente a), b), d) y e).
2. **Cambio de versión (Gemini):** el error de condiciones iniciales en Laplace (3.6 Thinking) no aparece en Hydrogen Thinking con ninguno de los dos prompts. La discrepancia principal del artículo depende de la versión del modelo.
3. **Problema c):** las cinco respuestas dan diseños distintos. Las cuatro con control proporcional discreto exceden el 10 % entre muestras sin advertirlo; la única que cumple las especificaciones en tiempo continuo es Gemini zero-shot.
4. **Lo que sí cambió con IDEAR:** respuestas más extensas, con tabla resumen y parámetros numéricos reportados (lo que exige la Estructura). En Gemini, IDEAR añadió la advertencia y(∞) = −0.25 que el zero-shot omitió y reportó valores simulados en c), aunque esta última instrucción figuraba explícitamente en la Referencia del prompt.
5. **Alcance:** una ejecución por combinación; los resultados describen casos y no permiten estimar efectos de IDEAR ni superioridad entre sistemas.
