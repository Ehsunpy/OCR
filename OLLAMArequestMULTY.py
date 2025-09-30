import ollama
import markdownify
def refine_and_mark_chat(text, chunk_size=CHUNK_SIZE):

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
            model="gemma3:12b",
            messages=messages,
            options={"temperature": 0.7}
        )
        reply = response.message.content
        all_responses.append(reply)
        messages.append({"role": "assistant", "content": reply})

    markdown_string = "\n\n---\n\n".join([markdownify.markdownify(r, heading_style='ATX') for r in all_responses])
    return markdown_string