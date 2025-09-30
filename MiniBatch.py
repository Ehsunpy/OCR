import json
import os
import sys
import time
import random
from tqdm import tqdm
from Gema_API import refine_and_mark

INPUT_DIR =sys.argv[1]  # مسیر پوشه حاوی فایل‌های JSON
OUTPUT_DIR = os.path.join(INPUT_DIR, "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def recommended_chunk_size(num_ctx=32000, reserve_tokens=300, chars_per_token=2):
    input_tokens = max(num_ctx - reserve_tokens, 0)
    return int(input_tokens * chars_per_token)


# CHUNK_SIZE = recommended_chunk_size(num_ctx=32000, reserve_tokens=300, chars_per_token=2)  # ~63k کاراکتر
def safe_chunk_size(max_tokens=32768, prompt_tokens=3000, reserve_tokens=3000, chars_per_token=2):
    """
    محاسبه اندازه امن هر chunk بر اساس ظرفیت کانتکست مدل
    """
    input_tokens = max_tokens - prompt_tokens - reserve_tokens
    return int(input_tokens * chars_per_token)

# استفاده
CHUNK_SIZE = safe_chunk_size(max_tokens=32768, prompt_tokens=3000, reserve_tokens=3000, chars_per_token=2) -500
print(f"✅ CHUNK_SIZE امن: {CHUNK_SIZE} کاراکتر")



def split_text(text: str, chunk_size: int):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def process_md(input_file):
    output_file = os.path.join(
        OUTPUT_DIR, os.path.basename(input_file).replace(".json", ".md")
    )

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for idx, text in enumerate(tqdm(data, desc=f"Processing {os.path.basename(input_file)}"), 1):
        if not text.strip():
            continue

        if len(text) <= CHUNK_SIZE:
            processed = refine_and_mark(text)
            results.append(processed)
        else:
            chunks = split_text(text, CHUNK_SIZE)
            processed_chunks = []

            for i, chunk in enumerate(chunks, 1):
                processed_chunk = refine_and_mark(chunk)
                processed_chunks.append(processed_chunk)

                if i % 10 == 0:
                    time.sleep(random.uniform(2, 5))

                print(f"Processed chunk {i}/{len(chunks)} of item {idx}")

            results.append("\n\n---\n\n".join(processed_chunks))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(results))

    print(f"✅ پردازش تمام شد. خروجی در {output_file} ذخیره شد.")


if __name__ == "__main__":
    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    for json_file in tqdm(json_files, desc="Overall Progress"):
        process_md(os.path.join(INPUT_DIR, json_file))
