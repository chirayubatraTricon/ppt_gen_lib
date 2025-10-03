from ..base.node import Node
from ..state import PptGenerationState
from ..utils.system_prompts import PROMPTS
from ..utils.category_constants import CATEGORIES
from ..utils.llm import LLM

class GenerateSlideContent(Node[PptGenerationState]):
    name = "generate_slide_content"

    async def __call__(self, state: PptGenerationState):
        try:
            user_text = state["prompt_text"]
            category_key = state["category"]
            layouts = state["layouts"]
            uploaded_file_content = state["pdf_text"]
            base_prompt = PROMPTS.get("generate_slide_content")
            content_prompt = PROMPTS.get("reference_content")
            category_descr = CATEGORIES.get(category_key, "")
            prompt_for_content = f"{content_prompt}\n\nUser request: {user_text}\nCategory: {category_descr}\n\nUploaded file content: {uploaded_file_content}"
            print("1")
            ppt_raw_data = LLM.generate_text(prompt_for_content)
            prompt = f"{base_prompt}\n Raw content: {ppt_raw_data}\nUser request: {user_text}\n template: {layouts}"
            state["slide_json"] = LLM.generate_json(prompt)
        
        except Exception as e:
            print("Error occured while generating slide content")

        return state