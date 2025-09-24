import json
import os
import sys
import time
import random
from tqdm import tqdm
from local_llm import refine_and_mark

# INPUT_FILE = sys.argv[1]

OUTPUT_FILE = os.path.basename(INPUT_FILE).split('.json')[0] + ".md"
parent_dir = os.path.dirname(INPUT_FILE)
OUTPUT_FILE = os.path.join(parent_dir, OUTPUT_FILE)

def recommended_chunk_size(num_ctx=32000, reserve_tokens=300, chars_per_token=2):
    input_tokens = max(num_ctx - reserve_tokens, 0)
    return int(input_tokens * chars_per_token)

CHUNK_SIZE = recommended_chunk_size(num_ctx=32000, reserve_tokens=300, chars_per_token=2)  # ~63k کاراکتر

def split_text(text: str, chunk_size: int):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
def process_md(INPUT_FILE):
    # بارگذاری داده‌ها
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    # پردازش هر متن
    for idx, text in enumerate(tqdm(data, desc="Processing"), 1):
        if not text.strip():
            continue

        # اگر متن کوتاه است
        if len(text) <= CHUNK_SIZE:
            processed = refine_and_mark(text)
            results.append(processed)
        else:
            # بخش‌بندی متن طولانی
            chunks = split_text(text, CHUNK_SIZE)
            processed_chunks = []

            for i, chunk in enumerate(chunks, 1):
                processed_chunk = refine_and_mark(chunk)
                processed_chunks.append(processed_chunk)

                if i % 10 == 0:
                    time.sleep(random.uniform(2, 5))

                print(f"Processed chunk {i}/{len(chunks)} of item {idx}")

            # بعد از اتمام همه chunkها، به نتایج اضافه کن
            results.append("\n\n---\n\n".join(processed_chunks))

    # ذخیره نهایی در Markdown
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(results))

    print(f"✅ پردازش تمام شد. خروجی در {OUTPUT_FILE} ذخیره شد.")
if __name__ == "__main__":
    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    for json_file in tqdm(json_files, desc="Overall Progress"):
        process_md(os.path.join(INPUT_DIR, json_file))))