import streamlit as st
from server.utils import CATEGORIES

def main():
    st.header("PPT Generator")

    user_question = st.text_input("Ask your question")
    category = st.selectbox("Select the type of ppt you want", options=list(CATEGORIES.keys()))
    uploaded_reference_doc = st.file_uploader("Upload your reference doc:", type=["pdf"])
    uploaded_template_file = st.file_uploader("Upload your PowerPoint template:", type=["pptx"])
    generate_button = st.button("Generate Presentation")


    if not generate_button:
        return
    
    if not user_question:
        st.error("Please enter a prompt for the presentation.")
        return

    if not uploaded_template_file:
        st.error("Please upload a PowerPoint template.")
        return
    


if __name__ == "__main__":
    main()