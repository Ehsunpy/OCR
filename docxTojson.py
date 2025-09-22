import docx
import json
import sys
import os
import random
from tqdm import tqdm


def doc_to_json(docx_file):

    # گرفتن فولدر فایل ورد
    folder = os.path.dirname(docx_file)

    # ساخت اسم فایل خروجی
    output_filename = os.path.splitext(os.path.basename(docx_file))[0] + ".json"
    output_json = os.path.join(folder, output_filename)  # درست شد

    # باز کردن فایل ورد
    document = docx.Document(docx_file)

    # گرفتن متن همه پاراگراف‌ها
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]

    # ذخیره به صورت آرایه JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)

    print("✅ ذخیره شد:", output_json)
if __name__ == "__main__":
    folder_path =sys.argv[1]

    docx_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".docx")]
    emojis = ["🎉", "✨", "📄", "🚀", "🌟", "💾"]

    # tqdm حرفه‌ای با فرمت دلخواه و رنگ
    for file in tqdm(docx_files,
                     desc="🚀 در حال تبدیل فایل‌ها",
                     unit=" فایل",
                     ncols=120,
                     colour='cyan',
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} - {postfix}'):
        output_file = doc_to_json(file)

        # انتخاب یک شکلک تصادفی برای هر فایل
        emoji = random.choice(emojis)

        # چاپ اسم فایل بدون خراب کردن نوار پروگرس
