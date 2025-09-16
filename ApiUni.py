import requests
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

