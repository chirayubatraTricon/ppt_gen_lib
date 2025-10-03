import os
from ..state import PptGenerationState
from ..utils.category_constants import TEMPLATES_DIR
from ..base.node import Node

class SaveUploadedPath(Node[PptGenerationState]):
    name = "save_uploaded_path"

    async def __call__(self, state: PptGenerationState ):
        try:
            uploaded_file = state["uploaded_template"]
            os.makedirs(TEMPLATES_DIR, exist_ok=True)
            template_path = os.path.join(TEMPLATES_DIR, uploaded_file.name)
            with open(template_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            state["template_path"] = template_path

        except Exception as e:
            print("error occured in saving file path")

        return state
