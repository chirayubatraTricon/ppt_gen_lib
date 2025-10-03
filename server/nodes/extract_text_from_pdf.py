from ..base.node import Node
from ..state import PptGenerationState

from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ExtractTextFromPdf(Node[PptGenerationState]):
    name = "extract_text_from_pdf"
    
    async def __call__(self, state: PptGenerationState):
        try:
            pdf_file = state["uploaded_reference_doc"]
            reader = PdfReader(pdf_file)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=200,
            )
            state["pdf_text"] = text_splitter.split_text(text)

        except Exception as e:
            print("Error in extracting text from uploaded file")

        return state