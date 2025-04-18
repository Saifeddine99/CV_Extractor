"""
Main Streamlit application for CV extraction.
"""
import os
import json

import streamlit as st

from src.utils.file_utils import list_pdf_files
from src.pdf_processing.utils import is_text_based_pdf, display_pdf_from_path

from src.pdf_processing.direct_extraction_from_pdf import extract_from_pdf_file

from src.llm_extraction.fields_extraction import fields_extraction_json

from src.evaluation.evaluation_utils import evaluate_extraction

# Set page configuration to wide layout
st.set_page_config(layout="wide")

# --- Sidebar for PDF Upload or Labeled Data Testing ---
st.sidebar.header("Options")

test_on_labeled = st.sidebar.checkbox("Test on Labeled PDFs")

if test_on_labeled:
    test_type = st.sidebar.radio("Choose PDF Type", ["Text-based", "Image-based"])
    labeled_pdf_dir = f"data/labeled_pdfs/{test_type.lower().replace('-', '_')}/"
    labeled_pdf_files = list_pdf_files(labeled_pdf_dir)
    
    if labeled_pdf_files:
        selected_labeled_pdf = st.sidebar.selectbox("Select a Labeled PDF", labeled_pdf_files)
        pdf_path = os.path.join(labeled_pdf_dir, selected_labeled_pdf)
    else:
        pdf_path = None

else:

    uploaded_file = st.sidebar.file_uploader("Upload a CV PDF", type=["pdf"])

    if uploaded_file is not None:

        # Loop through all files and delete them in unlabeled_pdfs folder
        for filename in os.listdir("data/unlabeled_pdfs"):
            file_path = os.path.join("data/unlabeled_pdfs", filename)
            if os.path.isfile(file_path):  # Only delete files
                os.remove(file_path)

        # Save the uploaded file temporarily or process it directly from memory
        with open(f"data/unlabeled_pdfs/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.read())

        pdf_path = f"data/unlabeled_pdfs/{uploaded_file.name}"
        
    else:
        pdf_path = None



# --- Main Area for Processing and Display ---
st.title("Intelligent CV Extraction System")

if pdf_path:
    st.subheader("Processing PDF...")
    display_pdf_from_path(pdf_path)

    is_text = is_text_based_pdf(pdf_path)
    st.write("###")
    st.info(f"Detected PDF type: {'Text-based' if is_text else 'Image-based'}")
    st.write("###")

    filename = "temp_uploaded.pdf" if not(test_on_labeled) else selected_labeled_pdf
    raw_text = extract_from_pdf_file(pdf_path, filename)

    st.subheader("PDF to HTML conversion")
    st.html(raw_text)


    if test_on_labeled:
        json_file_name = selected_labeled_pdf.replace('.pdf', '.json')
        selected_json_file_path = f"data/labeled_pdfs/final_extraction_ground_truth/{json_file_name}"
        
        # Read the HTML file
        with open(selected_json_file_path, "r", encoding="utf-8") as f:
            json_ground_truth = json.load(f)
        
        st.markdown("""___""")
        st.subheader("Fields Extraction: Ground Truth")
        st.write("###")
        st.json(json_ground_truth)

    st.write("###")
    st.title("Fields extraction with LLMS:")
    st.write("###")

    col1, col2, col3 = st.columns(3, border=True)
    with col1:
        st.subheader("Llama3")
        extracted_fields = fields_extraction_json("llama3", raw_text) # extract_fields
        st.write(extracted_fields)
        if test_on_labeled:
            st.markdown("""___""")
            st.subheader("Evaluation:")
            st.write(evaluate_extraction(json_ground_truth, extracted_fields))


    with col2:
        st.subheader("Mistral")
        extracted_fields = fields_extraction_json("mistral", raw_text) # extract_fields
        st.write(extracted_fields)
        if test_on_labeled:
            st.markdown("""___""")
            st.subheader("Evaluation:")
            st.write(evaluate_extraction(json_ground_truth, extracted_fields))


    with col3:
        st.subheader("Deepseek-r1")
        extracted_fields = fields_extraction_json("deepseek-r1", raw_text) # extract_fields
        st.write(extracted_fields)
        if test_on_labeled:
            st.markdown("""___""")
            st.subheader("Evaluation:")
            st.write(evaluate_extraction(json_ground_truth, extracted_fields))

elif not test_on_labeled:
    st.info("Please upload a CV PDF or choose to test on labeled PDFs in the sidebar.")

elif test_on_labeled and not labeled_pdf_files:
    st.info(f"No labeled PDFs found in \"data/labeled_pdfs/{test_type.lower().replace('-', '_')}/\"")