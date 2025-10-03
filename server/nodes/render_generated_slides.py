import os
import json

from ..base.node import Node
from ..state import PptGenerationState

class RenderGeneratedSlides(Node[PptGenerationState]):
    name = "render_generated_slides"

    async def __call__(self, state: PptGenerationState):
        try:
            """Returns generated slides"""
            slide_json = state["slide_json"]
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join("slides.json")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(slide_json, indent=2, ensure_ascii=False))
            
            slides = slide_json.get("slides") if isinstance(slide_json, dict) else None
            if not slides:
                print("No 'slides' key found in LLM output.")
                return

        except Exception as e:
            print("Error while dumping ppt in local directory")
        
        return state
