import json
import os
import sys
import time
import random
from tqdm import tqdm
from Gema_API import refine_and_mark

INPUT_FILE = sys.argv[1]

OUTPUT_FILE = os.path.basename(INPUT_FILE).split('.json')[0] + ".md"
parent_dir = os.path.dirname(INPUT_FILE)

OUTPUT_FILE = os.path.join(parent_dir, OUTPUT_FILE)

CHUNK_SIZE = 5000  # حداکثر کاراکتر هر تیکه

def split_text(text: str, chunk_size: int):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)  # لیست از رشته‌ها

results = []

for idx, text in enumerate(tqdm(data, desc="Processing"), 1):
    if not text.strip():
        continue

    if len(text) <= CHUNK_SIZE:
        processed = refine_and_mark(text)  # ⚡ اینجا متن به تابع داده میشه
        results.append(processed)
    else:
        chunks = split_text(text, CHUNK_SIZE)
        processed_chunks = []
        for i, chunk in enumerate(chunks, 1):
            if i % 10 == 0:
                time.sleep(random.uniform(2, 5))
            processed_chunks.append(refine_and_mark(chunk))
            print(f"Processed chunk {i}/{len(chunks)} of item {idx}")

        results.append("\n\n".join(processed_chunks))  # ادغام تیکه‌ها با فاصله خط

# ذخیره نهایی در Markdown
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n\n".join(results))

print(f"✅ پردازش تمام شد. خروجی در {OUTPUT_FILE} ذخیره شد.")
