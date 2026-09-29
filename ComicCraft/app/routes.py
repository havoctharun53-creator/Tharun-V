from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.schemas import PromptRequest
from app.services.comic_service import generate_comic
from app.services.image_generator import generate_image

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None},
    )


@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        layout, pdf_path = generate_comic(data)
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={"layout": layout, "pdf_path": pdf_path},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):
    try:
        layout, pdf_path = generate_comic(payload)
        return {
            "success": True,
            "panels": layout,
            "pdf_path": pdf_path,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/test-image")
async def test_image(prompt: str = "A brave fox exploring an enchanted forest"):
    try:
        path = generate_image(prompt, 0)
        return {"success": True, "image_path": path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/download/{filename}")
async def download(filename: str):
    exports_dir = BASE_DIR / "static" / "exports"
    path = exports_dir / filename
    if not path.exists() or path.parent != exports_dir:
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(
        path=str(path),
        media_type="application/pdf",
        filename=filename,
    )


@router.get("/export-success")
async def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={},
    )
