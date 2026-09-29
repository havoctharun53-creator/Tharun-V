from datetime import datetime
from pathlib import Path

from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = BASE_DIR / "static" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _local_image_path(web_path: str) -> Path:
    relative = web_path.removeprefix("/static/")
    return BASE_DIR / "static" / relative


def _pdf_text(value: str) -> str:
    # FPDF's built-in Helvetica is Latin-1. Replace unsupported Unicode
    # characters from AI output rather than failing PDF export.
    return str(value).encode("latin-1", "replace").decode("latin-1")


def save_pdf(layout: list[dict]) -> str:
    filename = f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.pdf"
    output = EXPORTS_DIR / filename

    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, _pdf_text(f"Panel {panel['panel_number']}: {panel['title']}"))

        image_path = _local_image_path(panel["image_path"])
        if image_path.exists():
            pdf.image(str(image_path), x=20, y=40, w=170)

        pdf.set_y(145)
        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(0, 7, panel["scene_description"])

        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, _pdf_text(f"Caption: {panel['caption']}"))

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, panel["narration"])

    pdf.output(str(output))
    return f"/static/exports/{filename}"
