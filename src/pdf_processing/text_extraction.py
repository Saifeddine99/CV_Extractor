import fitz  # PyMuPDF

from PyPDF2 import PdfReader
from io import StringIO
from html import escape


def extract_text_from_pdf_PyMuPDF(pdf_path):
    """
    Extracts text content from a PDF file and returns it in HTML format.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text content formatted as HTML.
             Returns an empty string if the PDF cannot be opened or has no text.
    """
    try:
        doc = fitz.open(pdf_path)
        html_output = "<html>\n<head>\n<title>Extracted Text</title>\n</head>\n<body>\n"
        for page in doc:
            text = page.get_text("html")
            html_output += text
        html_output += "\n</body>\n</html>"
        doc.close()
        return html_output
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""
    


def extract_pdf_to_html_pyPDF(pdf_path):
    """
    Extracts text content from a PDF file and formats it as basic HTML.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: An HTML string containing the extracted text, or None if an error occurs.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            html_output = StringIO()
            html_output.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Extracted Text</title>\n</head>\n<body>\n")

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    # Basic formatting: paragraphs separated by <p> tags
                    paragraphs = text.split('\n\n')
                    for paragraph in paragraphs:
                        escaped_paragraph = escape(paragraph)
                        html_output.write(f"<p>{escaped_paragraph}</p>\n")

            html_output.write("</body>\n</html>\n")
            return html_output.getvalue()

    except FileNotFoundError:
        print(f"Error: File not found at '{pdf_path}'")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None