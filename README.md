# CV Extractor

A comprehensive tool for extracting information from CVs using various LLM models and PDF processing techniques.

## Project Structure

```
├── data/
│   ├── labeled_pdfs/      # PDFs with known ground truth
│   │   ├── text_based/    # Text-based PDFs
│   │   └── image_based/   # Image-based PDFs
│   └── unlabeled_pdfs/    # PDFs to be processed
├── src/
│   ├── pdf_processing/    # PDF text and image extraction
│   ├── llm_extraction/    # LLM-based information extraction
│   ├── evaluation/        # Evaluation metrics and ground truth
│   ├── utils/            # Utility functions
│   └── app.py            # Streamlit application
└── notebooks/            # Experimental notebooks
```

## Features

- PDF text extraction
- Image-based PDF processing
- Multiple LLM model support (Llama3, Mistral, Phi)
- Streamlit-based web interface
- Evaluation framework

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run src/app.py
```

## License

MIT License
