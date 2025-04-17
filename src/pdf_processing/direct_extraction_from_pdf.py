import base64
import os
import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


@st.cache_data(ttl=7200, show_spinner='PDF convertion to HTML.....')
def extract_from_pdf_file(pdf_path, filename):
    with open(pdf_path, "rb") as f:
        data = f.read()

    base64_string = base64.b64encode(data).decode("utf-8")

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": filename,
                        "file_data": f"data:application/pdf;base64,{base64_string}",
                    },
                    {
                        "type": "input_text",
                        "text": "Please extract the text from the following resume and format it as basic HTML, preserving the structure using appropriate HTML tags like <p>, <h2>, <ul>, <li>, etc. Do not add any styling. Only return the HTML code as response",
                    },
                ],
            },
        ]
    )

    return response.output_text