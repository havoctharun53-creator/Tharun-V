from pathlib import Path

from app.services.exporters import save_pdf
from app.services.layout_builder import build_comic_layout


def test_layout_builder(tmp_path, monkeypatch):
    outlines = [{
        "panel_number": 1,
        "title": "Beginning",
        "scene_description": "A fox enters the forest.",
        "image_prompt": "A fox in a forest",
    }]
    stories = [{
        "panel_number": 1,
        "title": "Beginning",
        "scene_description": "A fox enters the forest.",
        "caption": "Deep in the woods...",
        "narration": "Milo takes the first step.",
    }]

    layout = build_comic_layout(outlines, stories, ["/static/panels/panel_1.png"])

    assert len(layout) == 1
    assert layout[0]["title"] == "Beginning"
    assert layout[0]["narration"] == "Milo takes the first step."


def test_pdf_export(tmp_path, monkeypatch):
    import app.services.exporters as exporters

    monkeypatch.setattr(exporters, "EXPORTS_DIR", tmp_path)

    # FPDF can create a text-only page even when the image is absent.
    layout = [{
        "panel_number": 1,
        "title": "Test",
        "image_path": "/static/panels/missing.png",
        "scene_description": "A test scene.",
        "caption": "Test caption.",
        "narration": "Test narration.",
    }]

    result = save_pdf(layout)
    assert result.startswith("/static/exports/")
    assert (tmp_path / result.split("/")[-1]).exists()
