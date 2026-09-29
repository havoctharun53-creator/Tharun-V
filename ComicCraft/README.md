# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI + Jinja2 application that turns a user's story idea into a five-panel comic.

## Pipeline

1. Gemini Flash creates a structured five-panel outline.
2. Gemini Pro expands it into narration, captions, and dialogue.
3. Hugging Face text-to-image creates one illustration per panel.
4. The layout builder joins text + images.
5. FPDF2 creates a downloadable multi-page PDF.

The original project specification describes the same five-stage flow and FastAPI routes. See the supplied project document. 

## Project structure

```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routes.py
│   ├── schemas.py
│   └── services/
│       ├── comic_service.py
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── panels/
│   └── exports/
├── requirements.txt
├── requirements-local-diffusers.txt
├── .env.example
└── README.md
```

## 1. Install Python

Use Python 3.11 or newer.

Check:

```powershell
python --version
```

## 2. Open the project in VS Code

Open the `ComicCraft` folder.

VS Code terminal:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure API keys

Copy:

```text
.env.example
```

to:

```text
.env
```

Then add your Gemini API key and Hugging Face token.

For the easiest first test, you can use:

```text
IMAGE_PROVIDER=demo
```

This keeps the whole web/PDF pipeline testable without an image API. Real AI artwork requires `IMAGE_PROVIDER=huggingface` and a valid `HF_API_KEY`.

## 5. Run

From the project root:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## 6. Test in this order

Run the automated unit tests with:

```powershell
pip install pytest
pytest -q
```


### Test the UI without image API

Set:

```text
IMAGE_PROVIDER=demo
```

Keep a valid `GEMINI_API_KEY`.

Generate:

- Prompt: `A brave fox exploring an enchanted forest`
- Character: `Milo`
- Setting: `Enchanted forest`
- Tone: `adventurous`
- Art style: `comic book`

The app should create five panels and a PDF.

### Test image generation only

Open:

```text
http://127.0.0.1:8000/test-image?prompt=A%20brave%20fox%20in%20a%20magical%20forest
```

### Test the JSON API

Use `/docs` → `POST /generate-comic/json`.

Example:

```json
{
  "story_prompt": "A brave fox exploring an enchanted forest",
  "character_name": "Milo",
  "setting": "Enchanted forest",
  "tone": "adventurous",
  "art_style": "comic book"
}
```

## 7. Real AI images with Hugging Face

Set:

```text
IMAGE_PROVIDER=huggingface
HF_PROVIDER=auto
IMAGE_MODEL=stabilityai/stable-diffusion-3.5-large
```

Then restart Uvicorn.

The model is configurable because Hugging Face's currently available inference models/providers can change.

## 8. Optional local Diffusers mode

If you specifically want the original project's local Diffusers approach:

```powershell
pip install -r requirements-local-diffusers.txt
```

Then set:

```text
IMAGE_PROVIDER=local
LOCAL_IMAGE_MODEL=runwayml/stable-diffusion-v1-5
LOCAL_DEVICE=auto
```

A local diffusion model can require substantial disk space, RAM/VRAM, and generation time. A GPU is strongly recommended.

## Troubleshooting

### `GEMINI_API_KEY is missing`

Make sure `.env` exists in the project root and contains:

```text
GEMINI_API_KEY=...
```

Then restart Uvicorn.

### `HF_API_KEY is missing`

Either add the token or temporarily use:

```text
IMAGE_PROVIDER=demo
```

### PowerShell execution-policy error

Use Command Prompt, or run PowerShell as appropriate for your machine and activate the venv there.

### PDF has no images

Check that generated files exist in:

```text
static/panels/
```

### API docs

FastAPI automatically exposes interactive documentation at:

```text
http://127.0.0.1:8000/docs
```
