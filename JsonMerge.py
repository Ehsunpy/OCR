#!/usr/bin/env python3
import json
import os
import sys

def flatten_strings(obj):
    """رشته‌ها را از داخل ساختارهای تو در تو استخراج می‌کند."""
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, list):
        out = []
        for x in obj:
            out.extend(flatten_strings(x))
        return out
    if isinstance(obj, dict):
        out = []
        for v in obj.values():
            out.extend(flatten_strings(v))
        return out
    return []

def gather_json_files(args):
    files = []
    for a in args:
        if os.path.isdir(a):
            for f in os.listdir(a):
                if f.lower().endswith(".json"):
                    files.append(os.path.join(a, f))
        else:
            files.append(a)
    # فقط فایل‌هایی که واقعاً وجود دارند و json هستند نگه داشته می‌شوند
    files = [os.path.abspath(p) for p in files if os.path.isfile(p) and p.lower().endswith(".json")]
    return files

def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_jsons.py <folder_or_file1> [file2 ...]")
        sys.exit(1)

    inputs = sys.argv[1:]
    json_files = gather_json_files(inputs)

    if not json_files:
        print("هیچ فایل JSON معتبری پیدا نشد.")
        sys.exit(1)

    merged = []
    for p in json_files:
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️ رد شد (خطا در خواندن {p}): {e}")
            continue

        texts = flatten_strings(data)
        for t in texts:
            s = t.strip()
            if s:
                merged.append(s)

    # تعیین مسیر خروجی: اگر آرگومان اول پوشه بود، خروجی در آن پوشه؛ در غیر این صورت در پوشه اولین فایل
    first_arg = inputs[0]
    if os.path.isdir(first_arg):
        out_dir = os.path.abspath(first_arg)
    else:
        out_dir = os.path.dirname(os.path.abspath(json_files[0]))

    out_path = os.path.join(out_dir, "merged.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"✅ تمام شد — {len(merged)} رشته در '{out_path}' ذخیره شد.")

if __name__ == "__main__":
    main()
