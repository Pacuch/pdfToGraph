import json
import ollama
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def process_page(page_json):
    """
    Send page JSON to Ollama model and return judgment/structure.
    """
    prompt = f"""
Here is a page of a book:

{json.dumps(page_json, indent=4)}

Does this page contain useful Table of Contents / structural info?
If yes, extract as a Markdown table:
Section | Subsection | Page Start | Page End
If no, return "NOT USEFUL".
    """

    response = ollama.chat(
        model="book-structure",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"].strip()


if __name__ == "__main__":
    with open(PROJECT_ROOT / "data" / "extracted_jsons" / "HRCTofTheLung.json", "r", encoding="utf-8") as f:
        book = json.load(f)

    all_results = []
    pages = book.get('pages')
    # debug only
    pages = pages[10:]

    for page in pages:
        result = process_page(page)
        try:
            if result != "NOT USEFUL":
                all_results.append(result)
            print(f"Page {page['page_num']} - {page.get('content')[:60]} ->\n{result}\n")
        except TypeError:
            pass

    (PROJECT_ROOT / "book_structure.md").write_text("\n\n".join(all_results))

    # import markdown
    # html_output = markdown.markdown(markdown_table_string)
