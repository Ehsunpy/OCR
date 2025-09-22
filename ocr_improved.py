"""
OCR API Module
-------------
This module provides functionality for extracting text from PDF files using
the alefba.roshan-ai.ir س AI OCR API service. It handles finding PDF files in a directory
and processing them through the OCR service.
"""
import sys
from tqdm import tqdm
import requests
import os
import json


class OcrApi:
    """OCR API client for processing PDF files and extracting text."""

    def __init__(
        self,
        api_url="https://alefba.roshan-ai.ir/api/read_document/",
        token="1d55fa5dfe5cfafdcd6b24fd6d516e7cdee7c4af",
        pdfs_dir=r"C:\Users\Ehsan\Desktop\ForLak1\Digtal\OcrAffterDigit\PDFs",
    ):
        """
        Initialize the OCR API client.

        Args:
            api_url (str): The OCR service API endpoint
            token (str): Authentication token for the API
            pdfs_dir (str): Directory containing PDF files to process
        """
        self.api_url = api_url
        self.token = token
        self.pdfs_dir = pdfs_dir
        self.file_paths = []

    def find_pdfs(self):
        """
        Find all PDF files in the specified directory.

        Returns:
            None: Updates self.file_paths with found PDF files
        """
        if not os.path.exists(self.pdfs_dir):
            print(f"Directory {self.pdfs_dir} not found!")
            return

        self.file_paths = [
            os.path.join(self.pdfs_dir, filename)
            for filename in os.listdir(self.pdfs_dir)
            if filename.lower().endswith(".pdf")
        ]

        print(f"Found {len(self.file_paths)} PDF files in {self.pdfs_dir}")
        for file_path in self.file_paths:
            print(f"   - {file_path}")

    def ocr_pdfs(self):
        """
        Process all found PDF files through the OCR service.

        Returns:
            list[str]: List of extracted texts for each PDF file
        """
        texts = []
        for file_path in tqdm(self.file_paths):
            print(f"\nProcessing: {file_path}")
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                texts.append("")
                continue
            try:

                headers = {"Authorization": f"Token {self.token}"}  # اینجا اصلاح شد
                with open(file_path, "rb") as f:
                    files = {
                        "document": (os.path.basename(file_path), f, "application/pdf")
                    }
                    response = requests.post(
                        self.api_url, headers=headers, files=files, timeout=500
                    )
                if response.status_code == 200:
                    response_data = response.json()
                    extracted_text = ""
                    if "pages" in response_data:
                        for page_num, page in enumerate(response_data["pages"], 1):
                            if "text" in page:
                                page_text = page["text"]
                                extracted_text += (
                                    f"--- Page {page_num} ---\n{page_text}\n\n"
                                )
                            elif "parts" in page:
                                for part in page.get("parts", []):
                                    if part.get("type") == "text" and "text" in part:
                                        extracted_text += part["text"] + "\n"
                    output_filename = os.path.splitext(os.path.basename(file_path))[0] + "_ocr.json"
                    output_path = os.path.join(self.pdfs_dir, output_filename)
                    
                    with open(output_path, "w", encoding="utf-8") as f:
                        
                        json.dump([extracted_text], f, ensure_ascii=False, indent=2)
                    texts.append(extracted_text.strip())
                    print(f"✅ OCR done: {file_path}")
                else:
                    print(f"❌ Error: {response.status_code}")
                    texts.append("")
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
                texts.append("")
        return texts
if __name__ == "__main__":
    ocr = OcrApi(pdfs_dir=sys.argv[1])
    ocr.find_pdfs()
    ocr.ocr_pdfs()