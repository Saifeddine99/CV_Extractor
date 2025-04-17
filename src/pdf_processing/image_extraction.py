import fitz
import os

def extract_text_from_image_pdf_html(pdf_path, language='eng'):
    """
    Extracts text content from an image-based PDF file using OCR
    and returns it in HTML format.

    Args:
        pdf_path (str): The path to the image-based PDF file.
        language (str, optional): The language code for OCR (e.g., 'eng' for English).
                                   Defaults to 'eng'. You might need to adjust this
                                   based on the language of your CVs.

    Returns:
        str: The extracted text content formatted as HTML.
             Returns an empty string if the PDF cannot be opened or OCR fails.
    """
    try:
        doc = fitz.open(pdf_path)
        html_output = "<html>\n<head>\n<title>Extracted Text (OCR)</title>\n</head>\n<body>\n"
        for page in doc:
            # Perform OCR on the page and get the text as a TextPage object
            textpage = page.get_textpage_ocr(flags=0, language=language)
            if textpage:
                html = textpage.extractHTML()
                html_output += html
        html_output += "\n</body>\n</html>"
        doc.close()
        return html_output
    except Exception as e:
        print(f"Error processing PDF for OCR: {e}")
        return ""

if __name__ == '__main__':
    # Example usage: Replace 'scanned_cv.pdf' with the actual path to your scanned PDF
    scanned_pdf_file = 'scanned_cv.pdf'
    extracted_html_ocr = extract_text_from_image_pdf_html(scanned_pdf_file)

    if extracted_html_ocr:
        print("Extracted HTML content (via OCR):")
        print(extracted_html_ocr)

        with open('extracted_scanned_cv.html', 'w', encoding='utf-8') as f:
            f.write(extracted_html_ocr)
        print("\nExtracted OCR content saved to extracted_scanned_cv.html")
    else:
        print("No text extracted via OCR or an error occurred.")