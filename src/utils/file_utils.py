"""
Utility functions for file handling.
"""
import os
from pathlib import Path
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def list_pdf_files(directory: str) -> List[str]:
    """
    Get all PDF files in a directory.
    
    Args:
        directory: Path to the directory
        
    Returns:
        List of PDF file paths
    """
    try:
        pdf_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(file)
        return pdf_files
    except Exception as e:
        logger.error(f"Error getting PDF files from {directory}: {str(e)}")
        return []



def create_directory(path: str) -> bool:
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: Path to the directory
        
    Returns:
        True if directory was created or already exists, False otherwise
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {path}: {str(e)}")
        return False



def save_json(data: dict, file_path: str) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import json
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {str(e)}")
        return False



def load_json(file_path: str) -> Optional[dict]:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the data or None if loading failed
    """
    try:
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {str(e)}")
        return None 