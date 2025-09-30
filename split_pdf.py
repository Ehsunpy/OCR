import os
import sys

from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, pages_per_split=15):
    # اسم فایل اصلی بدون پسوند
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # خوندن PDF
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    # تقسیم بندی
    for i in range(0, total_pages, pages_per_split):
        writer = PdfWriter()
        for j in range(i, min(i + pages_per_split, total_pages)):
            writer.add_page(reader.pages[j])

        # شماره نسخه (v0, v1, ...)
        part_number = i // pages_per_split
        output_filename = f"{base_name}_v{part_number}.pdf"

        with open(output_filename, "wb") as out_file:
            writer.write(out_file)

        print(f"✅ فایل ساخته شد: {output_filename}")


# مثال استفاده
split_pdf(sys.argv[1])
