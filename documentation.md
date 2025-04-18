# CV Information Extraction System Documentation

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Models](#models)
- [How Extraction Works](#how-extraction-works)
- [Accuracy Comparison](#accuracy-comparison)
- [AI Tools Used](#ai-tools-used)

## Setup Instructions

### Prerequisites

- Python 3.x
- Ollama installed for running local LLMs
- Required Python packages (install via pip):
  ```bash
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repository
2. Install the required dependencies
3. Ensure Ollama is running with the following models:
   - llama3
   - mistral
   - deepseek-r1

## Models

The system uses multiple models for different stages of extraction:

1. **Text Extraction Models**:

   - For both image-based and text-based PDFs, we use OpenAI's GPT-4.1 for optimal extraction results

2. **Field Extraction Models** (via Ollama):
   - Llama3
   - Mistral
   - Deepseek-r1

## How Extraction Works

The extraction process follows a multi-stage pipeline:

1. **PDF Type Detection**:

   - Uses the `is_text_based_pdf` function from `src/pdf_processing/utils.py`
   - Determines whether a PDF is text-based or image-based

2. **Text Extraction**:

   - Converts PDFs to HTML format
   - Different approaches were tested using Streamlit apps:
     - `src/evaluation/image_based_pdf_html_extraction_evaluation.py` for image-based PDFs
     - `src/evaluation/text_based_pdf_html_extraction_evaluation.py` for text-based PDFs
   - After extensive testing, GPT-4.1 was selected as the optimal solution for both PDF types

3. **Fields Extraction**:
   - Uses the `fields_extraction_json` function from `src/llm_extraction/fields_extraction.py`
   - Processes the extracted text through three different LLMs:
     - Llama3
     - Mistral
     - Deepseek-r1

## Accuracy Comparison

Based on our evaluation results, here are the average performance metrics for each model:

### Overall Model Performance

| Model       | Precision | Recall | F1 Score |
| ----------- | --------- | ------ | -------- |
| llama3      | 0.69      | 0.62   | 0.65     |
| mistral     | 0.71      | 0.69   | 0.70     |
| deepseek-r1 | 0.58      | 0.53   | 0.55     |

### Detailed Evaluation

For detailed evaluation results and visualizations:

1. Run the evaluation report:
   ```bash
   streamlit run src/evaluation/evaluation_report.py
   ```
2. This will display:
   - Interactive performance comparison charts
   - Detailed metrics for each CV
   - Model performance breakdowns by CV type

The evaluation data is generated using the `models_comparison.py` script and stored in `evaluation.json`.

## AI Tools Used

The development of this project was supported by several AI tools:

1. **Cursor AI**: Primary development environment
2. **ChatGPT**: Used for code optimization and problem-solving
3. **Google Gemini**: Additional development support

These tools were used to enhance development efficiency while maintaining code quality and best practices.
