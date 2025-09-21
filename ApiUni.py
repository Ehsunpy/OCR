import os.path

import requests
import json
import sys

from tqdm import tqdm


def PdfToText(pdf_path):
    url = "http://78.38.161.78:3085/ocr"
    # pdf_path = "m.pdf"
    payload = {
        "token": "1qaz@WSX3edc#RFV5tgb^YHN"
    }

    try:
        with open(pdf_path, "rb") as pdf_file:
            files = {
                "image": (pdf_path, pdf_file, "application/pdf")
            }
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
            print("Success!")
            print("Status Code:", response.status_code)
            print("Response JSON:", response.json())
            return response.json()
    except FileNotFoundError:
        print(f"Error: The file was not found at {pdf_path}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def save_json(data, path):
    """ذخیره داده در فایل JSON"""
    try:
        with open(path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
        print(f"Saved JSON to {path}")
    except Exception as e:
        print(f"Error while saving JSON: {e}")
if __name__ == "__main__":
    path=sys.argv[1]
    base_files =os.listdir(path)
    base_files = [i for i in base_files if i.endswith('.pdf')]
    for i in tqdm(base_files):
        pdf_file = os.path.join(path, i)
        os.path.basename(pdf_file)
        output_json = f"{pdf_file}.json"

        result = PdfToText(pdf_file)
        if result:
            save_json(result, output_json)