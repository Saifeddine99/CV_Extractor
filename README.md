# CV Extractor

A comprehensive tool for extracting Name, Email, Phone, Education, Skills and Experience from CVs using various LLM models (Llama3, Mistral, Deepseek-R1) and PDF processing techniques.

## Tutorial

Watch our tutorial video to see how the interface works:
[![CV Extractor Tutorial](https://img.youtube.com/vi/vIJnzV1sH7I/0.jpg)](https://www.youtube.com/watch?v=vIJnzV1sH7I)

## Project Structure

```
├── data/
│ ├── labeled_pdfs/ # PDFs with known ground truth
│ │ ├── text_based/ # Text-based PDFs
│ │ └── image_based/ # Image-based PDFs
│ └── unlabeled_pdfs/ # PDFs to be processed
├── src/
│ ├── pdf_processing/ # PDF text and image extraction
│ ├── llm_extraction/ # LLM-based information extraction
│ ├── evaluation/ # Evaluation metrics and ground truth
│ ├── utils/ # Utility functions
│ └── app.py # Streamlit application
├── requirements.txt # Python dependencies
└── run.sh # Automated setup and launch script
```

## Features

- PDF text extraction
- Image-based PDF processing
- Multiple LLM model support (Llama3, Mistral, Phi)
- Streamlit-based web interface
- Evaluation framework

## Installation & Usage

You have two options to set up and run the application:

### Option 1: Automated Setup (Recommended)

1. Make sure you have Python 3.8 or higher installed
2. Install Ollama following the instructions in the "Install Ollama" section below
3. Make the run script executable:
   ```bash
   chmod +x run.sh
   ```
4. Run the automated setup script:
   ```bash
   ./run.sh
   ```
   This script will:
   - Create and activate a virtual environment
   - Install all dependencies
   - Start the Ollama service if not running
   - Download required models if not present
   - Launch the Streamlit application

### Option 2: Manual Setup

#### 1. System Requirements

- Python 3.8 or higher
- Windows/Linux/macOS
- At least 8GB RAM (16GB recommended for running larger models)
- NVIDIA GPU with CUDA support (recommended but not mandatory)

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Install Ollama

#### Windows

1. Download the latest Ollama installer from [Ollama's official website](https://ollama.ai/download)
2. Run the installer and follow the on-screen instructions
3. Add Ollama to your system PATH if not done automatically

#### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS

```bash
brew install ollama
```

#### 4. Download Required Models

After installing Ollama, download the required models:

```bash
# Download Llama3
ollama pull llama3

# Download Mistral
ollama pull mistral

# Download Phi
ollama pull phi
```

#### 5. Verify Installation

To verify that Ollama is working correctly:

```bash
ollama list
```

You should see the downloaded models listed.

## Usage

1. Start the Ollama service:

```bash
ollama serve
```

2. In a new terminal, run the Streamlit app:

```bash
streamlit run src/app.py
```

## Troubleshooting

- If you encounter memory issues, try using smaller models or reduce the context window size
- For GPU acceleration issues, ensure CUDA is properly installed and configured
- If Ollama service fails to start, check if the port 11434 is available
