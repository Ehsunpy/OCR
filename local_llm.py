import ollama
import markdownify

client = ollama.Client()


def refine_and_mark(ocr_text):
    '''
    شما ورودی تکست خام میدهدی و مدل زبانی اصلاحات لازم رو انجام خواهد داد
    :param ocr_text:
    :return:MarkDown
    '''

    # 1. ساخت کلاینت

    # model = "gemma3:12b"
    model = "gemma3:1b"
    messages = [
        {
            "role": "system",
            "content": f"""You are a highly skilled Persian language expert. Your task is to proofread and correct OCR-generated Persian text, ensuring accuracy, readability, and proper formatting.

    - Correct any spelling and grammar errors in the provided text.
    - Add punctuation where necessary to improve clarity.
    - Remove unnecessary line breaks within paragraphs.
    - Insert a line break at the beginning of each new high-level section to improve structure.
    - Ensure that LaTeX formulas remain in English and are not modified.
    - Convert any HTML tags into proper Markdown syntax.
    - Maintain the original content and meaning of the text.

    - Fix reversed or broken characters and words so that the text reads correctly from right to left.
    - Correct common OCR mistakes (e.g., incorrect letters, missing or extra diacritics).
    - Restore proper punctuation, spacing, and paragraph breaks.
    - Preserve the original meaning and structure of the text.
    - Remove unnecessary line breaks inside paragraphs, but keep logical breaks between sections.

    **Important:**
    Correct only the spelling mistakes and incorrect words.
    
    Keep the original meaning, tone, and style exactly as it is.
    
    Do not add, remove, or rewrite anything else.
    
    Return only the corrected text."

    - Do not modify the content itself; focus solely on corrections and formatting.
    - Ensure LaTeX formulas remain unchanged and are not translated.
    - Reconstruct tables properly if there are any.
    - Ensure tables render correctly in Markdown and are readable.

    - Provide the entire output strictly in valid Markdown format.
    - Output a single well-formatted Markdown text string.
    - Follow Persian grammar and punctuation rules carefully.
    - Prioritize readability and clarity.

    Please provide only the corrected text in Markdown format as the final output, without any extra explanations or notes.
    Ensure output regenerate MarkDown to me
    This is the raw text:
    """
        },
        {
            "role": "user",
            "content": f"{ocr_text}"
        }
    ]

    response = client.chat(
        model=model,
        messages=messages,
        options={"temperature": 0.7}
    )

    print(response.message.content)
    markdown_string = markdownify.markdownify(response.message.content, heading_style='ATX')
    return markdown_string
