#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5  # Wait for Ollama to start
fi

# Check if required models are installed
required_models=("llama3" "mistral" "phi")
for model in "${required_models[@]}"; do
    if ! ollama list | grep -q "$model"; then
        echo "Downloading $model model..."
        ollama pull "$model"
    fi
done

# Start the Streamlit app
echo "Starting the application..."
streamlit run src/app.py 