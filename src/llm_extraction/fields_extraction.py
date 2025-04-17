import json
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda


def extract_json_from_response(text: str):
    """
    Attempts to extract JSON content from a string.
    It looks for the first '{' and the last '}' and tries to parse the content in between.
    If successful, it returns the parsed JSON. Otherwise, it returns the original text.
    """
    try:
        start_index = text.find("{")
        end_index = text.rfind("}")
        if start_index != -1 and end_index != -1 and start_index < end_index:
            json_string = text[start_index : end_index + 1]
            return json.loads(json_string)
        else:
            return text
    except json.JSONDecodeError:
        return text



@st.cache_data(ttl=36000, show_spinner='Fields Extraction.....')
def fields_extraction_json(model, html_cv):

    # Example structured output format (for guidance in the prompt)
    example_json = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1 (555) 123-4567",
        "education": [
            {
                "degree": "Bachelor of Science",
                "field": "Computer Science",
                "institution": "University of Example",
                "year": "2020"
            }
        ],
        "experience": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "duration": "2020-2023",
                "description": "Developed and maintained web applications"
            }
        ],
        "skills": ["Python", "JavaScript", "SQL", "Machine Learning"]
    }

    # Defining the prompt template
    prompt_template = ChatPromptTemplate.from_template("""
    You are an expert information extraction assistant.
    Given the following HTML-formatted resume, carefully extract the following fields and output them as a valid JSON object:
    - name (string)
    - email (string)
    - phone (string)
    - education (list of objects with "degree", "field", "institution", and "year")
    - experience (list of objects with "title", "company", "duration", and "description")
    - skills (list of strings)

    Ensure that all specified fields are present in the JSON output, even if the corresponding information is not found in the resume (in which case, the value should be an empty string or an empty list as appropriate for the field type).

    Here is an example of the JSON structure you MUST follow:
    ```json
    {example_json}
    ```

    Now, extract the information from the following HTML content:
    ```html
    {html_input}
    ```

    Important: Your ENTIRE response MUST be a valid JSON object. Do not include any other text or explanations before or after the JSON.
    """)

    model = OllamaLLM(model=model)

    output_parser = StrOutputParser()
    chain = (
        {
            "html_input": lambda x: x["html"],
            "example_json": lambda x: json.dumps(example_json, indent=4)
        }
        | prompt_template
        | model
        | output_parser
        | RunnableLambda(extract_json_from_response)  # Apply the JSON extraction function
    )
    
    response = chain.invoke({"html": html_cv})

    return response