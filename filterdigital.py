import os
import shutil
import sys

from PyPDF2 import PdfReader

def is_digital_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if not text or text.strip() == "":
                return False  # یه صفحه متن نداره → احتمالا اسکن
        return True  # همه صفحات متن دارن → دیجیتال
    except Exception as e:
        print(f"❌ خطا در خواندن {pdf_path}: {e}")
        return False

def separate_digital_pdfs(input_dir):
    digital_dir = os.path.join(input_dir, "digital_pdfs")
    os.makedirs(digital_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(input_dir, file)
            result = is_digital_pdf(file_path)
            if result is True:
                print(f"📄 دیجیتال: {file}")
                shutil.move(file_path, os.path.join(digital_dir, file))
            elif result is False:
                print(f"🖼 نیاز به OCR یا ترکیبی: {file}")
            else:  # None یعنی خطا در باز کردن
                print(f"⚠️ فایل {file} منتقل نشد!")
    # for file in os.listdir(input_dir):
    #     if file.lower().endswith(".pdf"):
    #         file_path = os.path.join(input_dir, file)
    #         if is_digital_pdf(file_path):
    #             print(f"📄 دیجیتال: {file}")
    #             shutil.move(file_path, os.path.join(digital_dir, file))
    #         else:
    #             print(f"🖼 نیاز به OCR یا ترکیبی: {file}")

# مثال استفاده:
input_dir = sys.argv[1]
separate_digital_pdfs(input_dir)
