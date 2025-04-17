import os
from pdf2image import convert_from_path
from PIL import Image, ImageFilter

def convert_to_scanned_pdf(input_folder, output_folder):
    """
    Converts all text-based PDF files in the input folder to scanned-looking
    PDFs and saves them in the output folder.

    Args:
        input_folder (str): Path to the folder containing text-based PDFs.
        output_folder (str): Path to the folder where scanned PDFs will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            if not os.path.exists(output_path):
                try:
                    # Convert PDF pages to images
                    images = convert_from_path(input_path)
                    scanned_images = []

                    for img in images:
                        # Apply a subtle blur to simulate a scan
                        blurred_image = img.filter(ImageFilter.GaussianBlur(radius=1))
                        scanned_images.append(blurred_image)

                    # Save the images as a new PDF
                    scanned_images[0].save(output_path, "PDF", resolution=100.0, save_all=True, append_images=scanned_images[1:])

                    print(f"Successfully converted '{filename}' to a scanned PDF.")

                except Exception as e:
                    print(f"Error processing '{filename}': {e}")
            else:
                print("file already created!")

if __name__ == "__main__":
    input_folder = "data/labeled_pdfs/text_based"
    output_folder = "data/labeled_pdfs/image_based"
    convert_to_scanned_pdf(input_folder, output_folder)
    print(f"\nConversion process finished. Scanned PDFs saved in '{output_folder}'.")