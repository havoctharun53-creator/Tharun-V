from app.schemas import ComicPanel


def build_comic_layout(
    outlines: list[dict],
    stories: list[dict],
    image_paths: list[str],
) -> list[dict]:
    story_by_number = {item["panel_number"]: item for item in stories}
    layout = []

    for outline, image_path in zip(outlines, image_paths):
        number = outline["panel_number"]
        story = story_by_number.get(number, {})
        panel = ComicPanel(
            panel_number=number,
            title=story.get("title", outline["title"]),
            image_path=image_path,
            scene_description=story.get(
                "scene_description", outline["scene_description"]
            ),
            image_prompt=outline["image_prompt"],
            caption=story.get("caption", ""),
            narration=story.get("narration", ""),
        )
        layout.append(panel.model_dump())

    return layout
