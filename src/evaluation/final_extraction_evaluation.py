import os
import json

import streamlit as st

from src.pdf_processing.utils import display_pdf_from_path

# Set page configuration to wide layout
st.set_page_config(layout="wide")

def get_pdf_names(folder_path):
    """Gets a list of PDF filenames from a folder, without the .pdf extension."""
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    return [os.path.splitext(f)[0] for f in pdf_files]

def read_json_file(file_path):
    """Reads and parses the content of a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return f"Error: File not found at '{file_path}'"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON in '{file_path}': {e}"
    except Exception as e:
        return f"An unexpected error occurred while reading '{file_path}': {e}"

# Paths to folders
pdf_folder = "data/labeled_pdfs/text_based"
json_folder_gt = "data/labeled_pdfs/final_extraction_ground_truth"

# Get list of PDF names
pdf_names = get_pdf_names(pdf_folder)


# Streamlit app
st.title("Data exraction evaluation")
st.write("###")

# Select PDF
selected_pdf_name = st.selectbox("Select a PDF", pdf_names)

selected_pdf_path = os.path.join(pdf_folder, f"{selected_pdf_name}.pdf")
selected_json_path_gt = os.path.join(json_folder_gt, f"{selected_pdf_name}.json")


st.write("###")
# Extract and display text in columns
col1, col2 = st.columns(2)

with col1:
    st.header("Actual PDF file")
    # Display PDF (placeholder)
    display_pdf_from_path(selected_pdf_path)

with col2:
    st.header("Ground Truth HTML")
    ground_truth_json = read_json_file(selected_json_path_gt)
    st.json(ground_truth_json)

