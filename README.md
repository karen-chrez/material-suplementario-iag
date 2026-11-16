# Material suplementario: IAG en Matemáticas Avanzadas

Material suplementario del artículo *The Use of Generative Artificial Intelligence in Advanced Mathematics Courses* (4.º CITCA).

## Contenido

| Carpeta | Contenido |
|---|---|
| `index.html` | Página principal: método, prompts, respuestas por problema, evaluación y verificación |
| `respuestas/` | 25 respuestas en PDF: `<problema>_<sistema>_<condición>.pdf` |
| `prompts/` | Prompts IDEAR tal como se enviaron y protocolo de aplicación |
| `verificacion/` | `verificacion.py`, su salida, versión MATLAB y evaluación detallada |
| `figuras/` | Figuras generadas por `verificacion.py` |

Claves de los archivos de respuesta: `gpt_zeroshot` (GPT-5.6 Sol, ago 2026), `gemini36_zeroshot` (Gemini 3.6 Thinking, ago–sep 2026), `geminiH_zeroshot` (Gemini Hydrogen Thinking, nov 2026), `gpt_idear` y `geminiH_idear` (nov 2026).

## Reproducir la verificación

```
pip install sympy numpy scipy control matplotlib
cd verificacion
python verificacion.py
```

Página: https://karen-chrez.github.io/material-suplementario-iag/
