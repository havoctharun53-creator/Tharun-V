from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.config import get_settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PANELS_DIR = BASE_DIR / "static" / "panels"
PANELS_DIR.mkdir(parents=True, exist_ok=True)


def _safe_name(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_")
    return value[:80] or "panel"


def _font(size: int):
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _demo_image(prompt: str, panel_number: int, output: Path) -> None:
    """
    Offline fallback so the UI/PDF pipeline remains testable without an HF token.
    This is deliberately not presented as an AI-generated image.
    """
    image = Image.new("RGB", (768, 768), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, 748, 748), outline="black", width=8)
    title_font = _font(42)
    body_font = _font(24)
    draw.text((55, 55), f"COMICCRAFT • PANEL {panel_number}", fill="black", font=title_font)
    wrapped = "\n".join(
        [prompt[i:i + 55] for i in range(0, min(len(prompt), 500), 55)]
    )
    draw.multiline_text((55, 150), wrapped, fill="black", font=body_font, spacing=12)
    draw.text((55, 650), "Demo image — configure HF_TOKEN for AI artwork.", fill="black", font=body_font)
    image.save(output, format="PNG")


def _huggingface_image(prompt: str, output: Path) -> None:
    settings = get_settings()
    if not settings.hf_api_key:
        raise RuntimeError("HF_API_KEY is missing.")

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        provider=settings.hf_provider,
        api_key=settings.hf_api_key,
    )
    image = client.text_to_image(
        prompt=prompt,
        model=settings.image_model,
    )
    image.save(output)


def _local_diffusers_image(prompt: str, output: Path) -> None:
    settings = get_settings()

    import torch
    from diffusers import StableDiffusionPipeline

    device = settings.local_device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    if device == "cpu":
        # CPU generation is possible but can be very slow.
        dtype = torch.float32
    else:
        dtype = torch.float16

    pipe = StableDiffusionPipeline.from_pretrained(
        settings.local_image_model,
        torch_dtype=dtype,
    )
    pipe = pipe.to(device)
    image = pipe(prompt, num_inference_steps=25, guidance_scale=7.5).images[0]
    image.save(output)


def generate_image(prompt: str, panel_number: int) -> str:
    settings = get_settings()
    filename = f"panel_{panel_number}_{_safe_name(prompt)[:45]}.png"
    output = PANELS_DIR / filename

    enhanced_prompt = (
        f"{prompt}. Cohesive comic panel, expressive characters, clear composition, "
        f"strong visual storytelling, clean line art, no readable text, {settings.app_name}."
    )

    if settings.image_provider.lower() == "huggingface":
        try:
            _huggingface_image(enhanced_prompt, output)
        except Exception:
            if settings.hf_api_key:
                raise
            _demo_image(prompt, panel_number, output)
    elif settings.image_provider.lower() == "local":
        _local_diffusers_image(enhanced_prompt, output)
    elif settings.image_provider.lower() == "demo":
        _demo_image(prompt, panel_number, output)
    else:
        raise RuntimeError(
            "IMAGE_PROVIDER must be one of: huggingface, local, demo."
        )

    return f"/static/panels/{filename}"
