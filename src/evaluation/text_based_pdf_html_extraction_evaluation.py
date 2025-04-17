import streamlit as st
import os

from src.pdf_processing.utils import display_pdf_from_path

from src.pdf_processing.text_extraction import extract_text_from_pdf_PyMuPDF, extract_pdf_to_html_pyPDF
from src.pdf_processing.direct_extraction_from_pdf import extract_from_pdf_file


# Set page configuration to wide layout
st.set_page_config(layout="wide")

def get_pdf_names(folder_path):
    """Gets a list of PDF filenames from a folder, without the .pdf extension."""
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    return [os.path.splitext(f)[0] for f in pdf_files]

def read_html_file(file_path):
    """Reads the content of an HTML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading HTML file: {e}"

# Paths to folders
pdf_folder = "data/labeled_pdfs/text_based"
html_folder_gt = "data/labeled_pdfs/pdf_to_html_ground_truth"

# Get list of PDF names
pdf_names = get_pdf_names(pdf_folder)

# Streamlit app
st.title("Text-Based PDF Text Extraction in HTML format")
st.write("###")

# Select PDF
selected_pdf_name = st.selectbox("Select a PDF", pdf_names)

selected_pdf_path = os.path.join(pdf_folder, f"{selected_pdf_name}.pdf")
selected_html_path_gt = os.path.join(html_folder_gt, f"{selected_pdf_name}.html")


# Display PDF (placeholder)
display_pdf_from_path(selected_pdf_path)

st.write("###")
# Extract and display text in columns
col11, col12 = st.columns(2)

with col11:
    st.header("Ground Truth HTML")
    st.write("###")
    
    ground_truth_html = read_html_file(selected_html_path_gt)
    st.markdown(ground_truth_html, unsafe_allow_html=True)

with col12:
    st.header("Extracted HTML PyMuPDF")
    st.write("###")

    try:
        extracted_html = extract_text_from_pdf_PyMuPDF(selected_pdf_path)
        #st.write(extracted_html)
        st.markdown(extracted_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error during extraction: {e}")
        st.write("Extraction failed.")



st.write("###")
st.markdown("""---""")
# Extract and display text in columns
col21, col22 = st.columns(2)

with col21:
    st.header("Ground Truth HTML")
    st.write("###")
    
    ground_truth_html = read_html_file(selected_html_path_gt)
    st.markdown(ground_truth_html, unsafe_allow_html=True)

with col22:
    st.header("Extracted HTML PyPDF2")
    st.write("###")

    try:
        extracted_html = extract_pdf_to_html_pyPDF(selected_pdf_path)
        st.markdown(extracted_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error during extraction: {e}")
        st.write("Extraction failed.")
    


st.write("###")
st.markdown("""---""")
# Extract and display text in columns
col31, col32 = st.columns(2)

with col31:
    st.header("Ground Truth HTML")
    st.write("###")
    
    ground_truth_html = read_html_file(selected_html_path_gt)
    st.markdown(ground_truth_html, unsafe_allow_html=True)

with col32:
    st.header("Extracted HTML with OpenAI and LangChain")
    st.write("###")

    extracted_result = extract_from_pdf_file(selected_pdf_path, selected_pdf_name + ".pdf")
    st.markdown(extracted_result, unsafe_allow_html=True)