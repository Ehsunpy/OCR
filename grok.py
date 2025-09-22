import markdownify
from groq import Groq
import arabic_reshaper
from bidi.algorithm import get_display


def reshape_fars(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


def refine_and_mark(ocr_text):


    client = Groq(api_key='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')

    prompt = f"""
    You are a highly skilled Persian language expert. Your task is to proofread and correct OCR-generated Persian text, ensuring that the final text is accurate, readable, and properly formatted.
  Your tasks:

      - Correct any spelling and grammar errors.
      - Add punctuation where necessary for clarity.
      - Remove unnecessary line breaks within paragraphs while keeping logical breaks between sections.
      - Insert a line break at the beginning of each high-level section to improve structure.
      - Ensure that **all formulas remain in proper LaTeX format** and are not modified.
      - Convert any HTML tags into proper Markdown syntax.
      - Reconstruct tables so that they render correctly in Markdown and are readable.
      - Preserve the original meaning and structure of the text.

      **Important:**

      - Do not modify the content itself; focus only on corrections and formatting.
      - Output must be a single, well-formatted Markdown string.
      - Follow Persian grammar and punctuation rules carefully.
      - Prioritize readability and clarity.
Ensure that the Persian text is displayed correctly from right to left, preserving proper character shaping and avoiding any garbled or reversed text.
        Do not add any extra text in the output and only return the processed  version of my original text.
      Here is the raw text to correct:
      {ocr_text}
      """


    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content":[{"type":"text","text": prompt}]}],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        reasoning_effort="default",
        stream=False,
    reasoning_format="hidden"   # ← درست شد
    )

    text = completion.choices[0].message.content
    markdown_string = markdownify.markdownify(text, heading_style='ATX')
    print(markdown_string)
    return markdown_string
