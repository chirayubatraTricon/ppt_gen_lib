# state.py
from langchain_core.messages import BaseMessage
from typing import TypedDict, List, Dict, Any, Optional

SAVE_UPLOADED_PATH_NODE = "SAVE_UPLOADED_PATH"
INSPECT_TEMPLATE_LAYOUT_NODE = "INSPECT_TEMPLATE_LAYOUT"
EXTRACT_TEXT_FROM_PDF_NODE = "EXTRACT_TEXT_FROM_PDF"
RENDER_GENERATED_SLIDES_NODE = "RENDER_GENERATED_SLIDES"
GENERATED_SLIDE_CONTENT_NODE = "GENERATED_SLIDE_CONTENT"

class PptGenerationState(TypedDict, total=False):
    prompt_text: str
    category: str
    uploaded_reference_doc: Optional[bytes]
    layouts: List[Dict]
    uploaded_template: Optional[bytes]
    template_path: str
    uploaded_doc_path: str
    pdf_text: str
    slide_json: str