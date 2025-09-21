# import base64
# from mistralai import Mistral
#
# # خواندن و کدگذاری فایل تصویر
# with open(r"C:\Users\Ehsan\Desktop\Screenshot 2025-09-14 052613.png", "rb") as f:
#     image_data = f.read()
#
# base64_image = base64.b64encode(image_data).decode("utf-8")
# image_url = f"data:image/jpeg;base64,{base64_image}"
#
# # پردازش تصویر کدگذاری شده
# client = Mistral(server_url="https://api.avalai.ir", api_key="aa-Imydoto5ch4iNs7ms1SotnusOvjrWc5bqTlIxrenJtHFWgUC",)
#
# # document_param = {"type": "image_url", "image_url": image_url}
# document_param = {"type": "document_url", "image_url": image_url}
#
# ocr_response = client.ocr.process(
#     model="mistral-ocr-latest",
#     document=document_param,
#     pages=list(range(0, 100)),  # پردازش تا 100 صفحه
#
#     retries=3,
# )
#
# print(ocr_response)

from mistralai import Mistral
import os
import base64
from mistralai import Mistral
file_path =r"E:\فورمت جدید\OCRRR\12-inbr.ir- دفتر مقررات ملی و کنترل ساختمان\دفتر مقررات ملی و کنترل ساختمانها\ایین نامه ها\PDFs\NotConvertedToWord\آئين نامه ماده 27 قانون نظام مهندسي و كنترل ساختمان مصوب 1379.pdf"

# خواندن و کدگذاری فایل PDF
with open(file_path, "rb") as f:
    pdf_data = f.read()

base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
document_url = f"data:application/pdf;base64,{base64_pdf}"
# پردازش PDF کدگذاری شده
client = Mistral(server_url="https://api.avalai.ir", api_key="aa-Imydoto5ch4iNs7ms1SotnusOvjrWc5bqTlIxrenJtHFWgUC",)

document_param = {"type": "document_url", "document_url": file_path}

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document=document_param,
    pages=list(range(0, 100)),  # پردازش تا 100 صفحه
    retries=3,
)

print(ocr_response)

pdfs_dir = os.path.dirname(file_path)
output_filename = os.path.splitext(os.path.basename(file_path))[0] + "_ocr.json"


print(ocr_response)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump([ocr_response], f, ensure_ascii=False, indent=2)
