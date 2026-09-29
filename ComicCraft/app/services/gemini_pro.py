from google import genai
from google.genai import types

from app.config import get_settings
from app.schemas import StoryResponse


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the .env file before generating a comic."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(
    outline: list[dict],
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
) -> list[dict]:
    settings = get_settings()
    prompt = f"""
Expand this comic outline into a polished comic script.

Original idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}

Outline:
{outline}

Return one object for every outline panel. Keep panel_number and title aligned
with the outline. Each panel needs:
- panel_number
- title
- scene_description
- caption: a short ambient/comic caption
- narration: concise narration and dialogue, suitable for a comic panel

Keep the plot coherent from panel 1 through panel {settings.panel_count}.
Use the character name naturally. Do not add markdown or commentary outside JSON.
""".strip()

    client = _client()
    response = client.models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.85,
            response_mime_type="application/json",
            response_schema=StoryResponse,
        ),
    )

    if not response.parsed:
        raise RuntimeError("Gemini returned no structured story.")
    return [panel.model_dump() for panel in response.parsed.panels]
