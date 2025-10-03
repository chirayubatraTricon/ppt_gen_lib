from langgraph.graph.state import CompiledStateGraph
from .base.builder import GraphBuilder
from .nodes import SaveUploadedPath, InspectTemplateLayout, ExtractTextFromPdf, RenderGeneratedSlides, GenerateSlideContent
from langgraph.graph import START, END


from .state import (
    PptGenerationState,
    SAVE_UPLOADED_PATH_NODE,
    INSPECT_TEMPLATE_LAYOUT_NODE,
    RENDER_GENERATED_SLIDES_NODE,
    EXTRACT_TEXT_FROM_PDF_NODE,
    GENERATED_SLIDE_CONTENT_NODE,
)


def get_ppt_generation_workflow(
    
) -> CompiledStateGraph:
    """
    Creates and compiles the PPT generation graph.

    Returns:
        CompiledStateGraph: A compiled graph ready for execution.
    """
     # Initialize the graph builder with the state schema
    builder = GraphBuilder(state_schema=PptGenerationState)

    save_uploaded_path = SaveUploadedPath()
    inspect_template_layout = InspectTemplateLayout()
    render_generated_slides = RenderGeneratedSlides()
    extract_text_from_pdf = ExtractTextFromPdf()
    generate_slide_content = GenerateSlideContent()

    builder.add_nodes({
         SAVE_UPLOADED_PATH_NODE: save_uploaded_path,
         INSPECT_TEMPLATE_LAYOUT_NODE: inspect_template_layout,
         EXTRACT_TEXT_FROM_PDF_NODE: extract_text_from_pdf,
         RENDER_GENERATED_SLIDES_NODE: render_generated_slides,
         GENERATED_SLIDE_CONTENT_NODE: generate_slide_content,
    })

    builder.add_edges([
        (START, SAVE_UPLOADED_PATH_NODE),
        (SAVE_UPLOADED_PATH_NODE, INSPECT_TEMPLATE_LAYOUT_NODE),
        (INSPECT_TEMPLATE_LAYOUT_NODE, EXTRACT_TEXT_FROM_PDF_NODE),
        (EXTRACT_TEXT_FROM_PDF_NODE, GENERATED_SLIDE_CONTENT_NODE),
        (GENERATED_SLIDE_CONTENT_NODE, RENDER_GENERATED_SLIDES_NODE),
        (RENDER_GENERATED_SLIDES_NODE, END)
    ])

    app = builder.compile()

    return app
