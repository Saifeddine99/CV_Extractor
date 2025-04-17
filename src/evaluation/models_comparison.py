import os
import random
import json

from src.pdf_processing.direct_extraction_from_pdf import extract_from_pdf_file
from src.llm_extraction.fields_extraction import fields_extraction_json
from src.evaluation.evaluation_utils import evaluate_extraction

# Define paths
text_based_dir = "data/labeled_pdfs/text_based"
image_based_dir = "data/labeled_pdfs/image_based"
ground_truth_dir = "data/labeled_pdfs/final_extraction_ground_truth"

# Function to randomly sample N PDF filenames from a directory
def sample_pdfs_from_dir(directory, n):
    all_files = [directory + "/" + f for f in os.listdir(directory) if f.endswith(".pdf")]
    return random.sample(all_files, min(n, len(all_files)))

# Sample 5 PDFs from each directory
text_pdfs = sample_pdfs_from_dir(text_based_dir, 5)
image_pdfs = sample_pdfs_from_dir(image_based_dir, 5)

# Combine both sets
selected_pdfs = text_pdfs + image_pdfs

# Load corresponding ground truth files
evaluation = {}

for pdf_file in selected_pdfs:
    pdf_filename = pdf_file.split("/")[-1]

    json_filename = os.path.splitext(pdf_filename)[0] + ".json"
    json_path = os.path.join(ground_truth_dir, json_filename)

    if os.path.exists(json_path):

        actual_data = {}

        with open(json_path, "r", encoding="utf-8") as f:
            actual_data = json.load(f)

        print(pdf_file)

        evaluation[pdf_file] = []

        try:
            print("text extraction in HTML format:")
            raw_text = extract_from_pdf_file(pdf_file, pdf_filename)

            try:
                print("prediction using Llama3:")
                prediction_llama3 = fields_extraction_json("llama3", raw_text)
                evaluation[pdf_file].append({"llama3": evaluate_extraction(actual_data, prediction_llama3)})
            except:
                evaluation[pdf_file].append({"llama3": {}})

            try:
                print("prediction using Mistral:")
                prediction_mistral = fields_extraction_json("mistral", raw_text)
                evaluation[pdf_file].append({"mistral": evaluate_extraction(actual_data, prediction_mistral)})
            except:
                evaluation[pdf_file].append({"mistral": {}})
            
            try:
                print("prediction using Deepseek-r1:")
                prediction_deepseek = fields_extraction_json("deepseek-r1", raw_text)
                evaluation[pdf_file].append({"deepseek-r1": evaluate_extraction(actual_data, prediction_deepseek)})
            except:
                evaluation[pdf_file].append({"deepseek-r1": {}})

        except:
            print(f"{pdf_filename} can't be converted to HTML")
    

        # Save the updated data
        with open("src/evaluation/evaluation.json", 'w') as f:
            json.dump(evaluation, f, indent=2)


    else:
        print(f"⚠️ Ground truth file not found for: {pdf_filename}")