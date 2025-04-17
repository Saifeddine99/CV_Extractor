import fitz  # PyMuPDF
import streamlit as st
import base64

def is_text_based_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text = page.get_text()
            if text.strip():  # If a page has non-whitespace text
                return True
        return False  # No selectable text found
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return False
    


def display_pdf_from_path(pdf_path: str):
    """Display a PDF file from a local path in a scrollable iframe."""
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")

        pdf_display = f'''
            <iframe src="data:application/pdf;base64,{base64_pdf}"
                    width="100%" height="800px" type="application/pdf">
            </iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"File not found: {pdf_path}")
    except Exception as e:
        st.error(f"An error occurred while displaying the PDF: {e}")
