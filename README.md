# Material suplementario: IAG en Matemáticas Avanzadas

Material suplementario del artículo *The use of Generative Artificial Intelligence in advanced mathematics courses* (4.º CITCA).

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

## Publicar

1. Crear un repositorio público en GitHub y subir todo el contenido de esta carpeta.
2. En **Settings → Pages**, elegir *Deploy from a branch*, rama `main`, carpeta `/ (root)`. La página queda en `https://<usuario>.github.io/<repositorio>/`.
3. Para el DOI: entrar a zenodo.org con la cuenta de GitHub, activar el repositorio en **GitHub → Repositories** y crear un *release* en GitHub. Zenodo archiva esa versión y le asigna un DOI.
4. Escribir el DOI en `index.html` (sección «Cómo citar») y en el artículo.

Si la revisión es doble ciego, usar mientras tanto una copia anónima (por ejemplo, anonymous.4open.science) y quitar los nombres de `index.html`.

## Licencia

Textos y figuras: CC BY 4.0. Código: MIT. Las respuestas fueron generadas por ChatGPT (OpenAI) y Gemini (Google) y se publican sin modificar.
