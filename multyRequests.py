import os
import json
import time
import random
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from OLLAMArequestMULTY import refine_and_mark_chat  # نسخه chat که چانک‌ها context دارند

INPUT_DIR = r'G:\path\to\json_folder'  # مسیر پوشه JSON ها
OUTPUT_DIR = os.path.join(INPUT_DIR, "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def recommended_chunk_size(num_ctx=32000, reserve_tokens=300, chars_per_token=2):
    input_tokens = max(num_ctx - reserve_tokens, 0)
    return int(input_tokens * chars_per_token)


CHUNK_SIZE = recommended_chunk_size(num_ctx=32000, reserve_tokens=300, chars_per_token=2)


def split_text(text: str, chunk_size: int):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def refine_and_mark_chat(text, chunk_size=CHUNK_SIZE):
    """
    پردازش متن طولانی به چانک و ارسال به مدل لوکال مثل یک چت
    """
    import ollama
    import markdownify
    client = ollama.Client()

    chunks = split_text(text, chunk_size)

    messages = [
        {"role": "system",
         "content": "You are a highly skilled Persian language expert. Correct OCR text, preserve meaning, output Markdown."}
    ]

    all_responses = []

    for chunk in chunks:
        messages.append({"role": "user", "content": chunk})
        response = client.chat(
            model="gemma3:1b",
            messages=messages,
            options={"temperature": 0.7}
        )
        reply = response.message.content
        all_responses.append(reply)
        messages.append({"role": "assistant", "content": reply})

    markdown_string = "\n\n---\n\n".join([markdownify.markdownify(r, heading_style='ATX') for r in all_responses])
    return markdown_string


def process_md_file(input_file):
    output_file = os.path.join(OUTPUT_DIR, os.path.basename(input_file).replace(".json", ".md"))

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for idx, text in enumerate(tqdm(data, desc=f"Processing {os.path.basename(input_file)}"), 1):
        if not text.strip():
            continue
        processed = refine_and_mark_chat(text)
        results.append(processed)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(results))

    print(f"✅ پردازش تمام شد. خروجی در {output_file} ذخیره شد.")


if __name__ == "__main__":
    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]

    # مالتی‌ترد: پردازش چند فایل JSON همزمان
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_file = {executor.submit(process_md_file, os.path.join(INPUT_DIR, f)): f for f in json_files}
        for future in tqdm(as_completed(future_to_file), total=len(future_to_file), desc="Overall Progress"):
            future.result()
