import os
import sys

from PyPDF2 import PdfReader
from docx import Document

import warnings
from PyPDF2.errors import PdfReadWarning
import unicodedata
import arabic_reshaper
from bidi.algorithm import get_display


def fix_persian_text(text):
    # نرمال‌سازی یونیکد
    text = unicodedata.normalize("NFKC", text)

    # تبدیل حروف Presentation Forms به حروف استاندارد
    reshaped_text = arabic_reshaper.reshape(text)

    # اصلاح جهت نمایش (راست به چپ)
    bidi_text = get_display(reshaped_text)

    return bidi_text


# نمونه استفاده


warnings.filterwarnings("ignore", category=PdfReadWarning)

def is_digital_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if not text or text.strip() == "":
                return False  # حداقل یک صفحه متن نداره → اسکن یا OCR
        return True
    except:
        return False
import re

def clean_text(text: str) -> str:
    # حذف کاراکترهای NULL و کنترل غیرقابل چاپ
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', ' ', text)

def extract_text_from_digital_pdfs(input_dir):
    text_dir = os.path.join(input_dir, "texts")
    os.makedirs(text_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(input_dir, file)

            if is_digital_pdf(file_path):
                print(f"📄 در حال استخراج متن از: {file}")
                try:
                    reader = PdfReader(file_path)
                    all_text = ""
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            all_text += page_text + "\n"

                    # ذخیره در فایل متنی با همان نام
                    docx_filename = os.path.splitext(file)[0] + ".docx"
                    docx_path = os.path.join(text_dir, docx_filename)
                    fixed_text = fix_persian_text(all_text)
                    all_text = clean_text(fixed_text)  # 🟢 پاکسازی متن

                    print(all_text)
                    document = Document()
                    # کل متن رو یک پاراگراف اضافه کن
                    document.add_paragraph(all_text)
                    document.save(docx_path)

                except Exception as e:
                    print(f"❌ خطا در پردازش {file}: {e}")

# مثال استفاده:
input_dir = sys.argv[1]
  # مسیر پوشه‌ی PDF ها
extract_text_from_digital_pdfs(input_dir)
