from app.schemas import PromptRequest
from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout


def generate_comic(request: PromptRequest) -> tuple[list[dict], str]:
    outline = generate_outline(
        request.story_prompt,
        request.character_name,
        request.setting,
        request.tone,
        request.art_style,
    )

    story = generate_story(
        outline,
        request.story_prompt,
        request.character_name,
        request.setting,
        request.tone,
    )

    image_paths = [
        generate_image(panel["image_prompt"], panel["panel_number"])
        for panel in outline
    ]

    layout = build_comic_layout(outline, story, image_paths)
    pdf_path = save_pdf(layout)
    return layout, pdf_path
