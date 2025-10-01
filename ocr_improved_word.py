import sys

import requests
import os
from tqdm import tqdm

class OcrToWord:
    def __init__(self, token, pdfs_dir):
        self.read_url = "https://alefba.roshan-ai.ir/api/read_document/"
        self.word_url = "https://alefba.roshan-ai.ir/api/download_word/"
        self.token = token
        self.pdfs_dir = pdfs_dir
        self.headers = {"Authorization": f"Token {self.token}"}

    def process_pdfs(self):
        pdf_files = [f for f in os.listdir(self.pdfs_dir) if f.lower().endswith(".pdf")]
        print(f"📂 Found {len(pdf_files)} PDF files")

        for file_name in tqdm(pdf_files, desc="Processing PDFs"):
            file_path = os.path.join(self.pdfs_dir, file_name)
            try:
                # مرحله ۱: آپلود و پردازش
                with open(file_path, "rb") as f:
                    files = {"document": (file_name, f, "application/pdf")}
                    resp = requests.post(self.read_url, headers=self.headers, files=files, timeout=600)

                if resp.status_code != 200:
                    print(f"❌ Error in read_document: {resp.status_code} - {resp.text}")
                    continue

                data = resp.json()
                document_url = data.get("document_url")
                if not document_url:
                    print(f"❌ No document_url in response: {data}")
                    continue

                # مرحله ۲: دریافت فایل ورد
                resp_word = requests.post(self.word_url, headers=self.headers, data={"document_url": document_url}, timeout=600)
                if resp_word.status_code == 200:
                    output_dir = os.path.join(os.getcwd(), "output_word")
                    os.makedirs(output_dir, exist_ok=True)

                    filename = os.path.splitext(os.path.basename(file_path))[0] + "_ocr.docx"
                    output_path = os.path.join(output_dir, filename)
                    with open(output_path, "wb") as f:
                        f.write(resp_word.content)
                    print(f"✅ Word saved: {output_path}")
                else:
                    print(f"❌ Error in download_word: {resp_word.status_code} - {resp_word.text}")

            except Exception as e:
                print(f"❌ Exception on {file_name}: {e}")


if __name__ == "__main__":

    token = "e7bf08c5b2e221c86d76ab2a697801672be7f4d3"

    pdfs_dir =sys.argv[1]
    client = OcrToWord(token=token, pdfs_dir=pdfs_dir)
    client.process_pdfs()
