from openai import OpenAI
import markdownify
def refine_and_mark(ocr_text):
    '''
    شما ورودی تکست خام میدهدی و مدل زبانی اصلاحات لازم رو انجام خواهد داد
    :param ocr_text:
    :return:MarkDown
    '''
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key="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",
    )
    # برای مثال یک متن که تبدیل شده
#     ocr_text = """
# Out[39]: ['--- Page 1 ---\n\n\n\n\nجمهوری اسلامی ایران\nوزارت راه و ترابری.\n\nسازمان راهداری و حمل و نقل جاده ای،\n\nادارات کل / سازمان حمل و نقل و پایانه های سراسر کشور\n\nموضوع : اصلاح ماده ۱۱ ضوابط حمل و نقل مسافر\n\nبا سلام\n\nشماره :\nتاریخ ، ،\nپیوست :\n\n\n\n۱۷۱\n\n۱۰۰۵\n\n--۱۳۸۶-۸%-۲۲\nنرارب.\n\nبه استناد ماده ۹آیین نامه حمل بار و مسافر و مدت لغو پروانه فعالیت و تعطیلی موسسات\nحمل و نقل جاده ای و تفویض اختیار مقام عالی وزارت به شماره ۷۹۳۷/۱۱ مورخ ۷۹/۶/۲۷ ، ماده ۱۱ ضوابط\nحمل و نقل مسافر موضوع ماده ۹ آیین نامه باد شده به شرح زیر اصلاح می گردد :\n\nماده ۱۱ -شرکتها و موسسات مسافربری مکلفند قبل از برقراری سرویس و صدور بلیت در مسیرهای،\nمختلف نسبت به ایجاد شعبه و یا عقد قرارداد نمایندگی با سایر شرکتها و موسسات مسافربری همنام\nاقدام لمایند.\n\nتبصره (۱) -همنامی عبارتست از انتخاب نام یکسان برای شرکتهای همکار .\n\nتبصره (۲) - به مجموعه شرکتهای حمل و نقل مسافر که نحت نام واحد در سراسر کشور فعالیت می نمایند\nشبکه شرکتهای مسافربری إطلاق می شود .\n\nتبصره (۳) - شرکت دارنده پام اصلی شرکتی است که دارای تقدم زمانی در لبت نام مزبور است .\nتبصره (۴) - هر شرکت مسافربری می تواند صرفا یک لمایلده هملام یا یک شعبه در شهر مقصد داشته\nباشد . هرگاه در شهر مقصد بیش از یک پایانه عمومی مسافری وجود داشته باشد ، شرکت می تواند در\nهر یک از پایانه های موصوف دارای یک نمایلده هملام باشد .\n\nاجرای این اصلاحیه مطابق برنامه زمانبندی و دستورالعمل اجرائی خواهد بود که متعاقباً توسط دفتر\nحمل و نقل کالا و مسافر تهیه و ابلاغ می گردد . کلیه شرکتها و موسساتی که پس از ابلاغ دستورالعمل\nآدرس: تهران - بلوار کشاورز - خیابان فلسطین جلوبی - خیابان دمشق - پلاک ۱۹ تلفن ۸۸ - ۸۸۸۰۴۳۷۹\nکدپستی: ۱۴۱۶۷۵۳۹۴۱ -صندوق پستی : ۳۷۷۳-۱۴۱۵۵\n\n--- Page 2 ---\n\n\n| جمهوری اسلامی ایران  | شماره :  |\n| وزارت راه و ترابری.  | تاریخ :  |\n| سازمان راهداری و حمل و نقل جاده ای  | پیوست ،  |\n\nاجرایی این اصلاحیه توسط دفتر حمل و نقل کالا و مسافر مشمول اجرای طرح همنامی می شوند در صورت\nعدم تمایل به اعطای نمایندگی به شرکتهای همنام در مقصد می توانند از تسهیلات ویژه تأسیس شعب\nمندرج در تبصره ۲ و ۵ ماده ۱۴ و تبصره ۴ و ۵ ماده ۱۵ و همچنین ماده ۱۶ بخشنامه شماره ۸۷۳۵/۷۱\n\nمورخ ۸۱/۲/۱۸ بهره مند شوند .\n\n\n\n\n\n/ محمد بخارایر\n\nمعاون وزیر و رئیس سازمان\n\nرونوشت :\n\n- اعضاء محترم هیأت عامِل برای آگاهی\n- فرمانده محترم پلیس راه برای آگاهی\n- اداره کل حراست برای اطلاع\n\n- دفتر ریاست و روابط عمومی برای اطلاع\n- دفتر حقوقی و تدوین مقررات برای اطلاع\n\n- دفتر حمل و نقل کالا و مسافر برای اطلاع و اقدام لازم\nاقدام کننده : آقای آدم نژاد\n\nآدرس: تهران - بلوار کشاورز - خیابان فلسطین جلوبی - خیابان دمشق - پلاک ۱۹ تلفن ۸۸ - ۸۸۸۰۴۳۷۹\nکدپستی: ۱۴۱۶۷۵۳۹۴۱ -صندوق پستی: ۳۷۷۳-۱۴۱۵۵']
#
#     """

    completion = client.chat.completions.create(
      model="qwen/qwen3-30b-a3b:free",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": f"""You are a highly skilled Persian language expert. Your task is to proofread and correct OCR-generated Persian text, ensuring accuracy, readability, and proper formatting.

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

- Do not modify the content itself; focus solely on corrections and formatting.
- Ensure LaTeX formulas remain unchanged and are not translated.
- Reconstruct tables properly if there are any.
  - Ensure tables render correctly in Markdown and are readable.

- Provide the entire output strictly in valid Markdown format.
- Output a single well-formatted Markdown text string.
- Follow Persian grammar and punctuation rules carefully.
- Prioritize readability and clarity.

Please provide only the corrected text in Markdown format as the final output, without any extra explanations or notes.

 This is the raw text:
    {ocr_text}
    """
            }
          ]
        }
      ]
    )

    print(completion.choices[0].message.content)
    markdown_string = markdownify.markdownify(completion.choices[0].message.content, heading_style='ATX')
    return markdown_string
    # 3
# markdown_string = refine_and_mark()
# with open('sample4.md', 'w',encoding="utf-8") as f:
#     f.write(markdown_string)