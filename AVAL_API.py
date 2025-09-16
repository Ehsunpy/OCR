import base64
from mistralai import Mistral

# خواندن و کدگذاری فایل تصویر
with open(r"C:\Users\Ehsan\Desktop\Screenshot 2025-09-14 052613.png", "rb") as f:
    image_data = f.read()

base64_image = base64.b64encode(image_data).decode("utf-8")
image_url = f"data:image/jpeg;base64,{base64_image}"

# پردازش تصویر کدگذاری شده
client = Mistral(server_url="https://api.avalai.ir", api_key="aa-Imydoto5ch4iNs7ms1SotnusOvjrWc5bqTlIxrenJtHFWgUC",)

# document_param = {"type": "image_url", "image_url": image_url}
document_param = {"type": "document_url", "image_url": image_url}

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document=document_param,
    pages=list(range(0, 100)),  # پردازش تا 100 صفحه

    retries=3,
)

print(ocr_response)