import argparse
import json
import os
import string
import sys
from collections import defaultdict
from pathlib import Path
import fitz
from typing import Union, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # project folder
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import PROJECT_ROOT

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.logger.document_reader import document_logger

# set logger to debug level
document_logger.setLevel(
    os.getenv("DOCUMENT_LOG_LEVEL", "DEBUG").upper()
)

def count_words_in_text(text: str) -> int:
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.translate(translator)

    words = clean_text.split()
    return len(words)


def get_json_depth(obj, level=1):
    """Recursively calculate the maximum depth of a JSON-serializable object."""
    if isinstance(obj, dict):
        if not obj:
            return level
        return max(get_json_depth(v, level + 1) for v in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return level
        return max(get_json_depth(i, level + 1) for i in obj)
    else:
        return level


def save_content_to_file(content: Union[str, dict, list], file_path: Union[Path, str]):
    """
    Save content to a file, automatically handling JSON or plain text.
    For JSON files, indent is dynamic based on structure depth.
    """
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix.lower() == ".json":
            # If content is a string, try parsing it
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    raise ValueError("Provided string is not valid JSON.")

            # Dynamic indent: deeper structures -> larger indent
            depth = get_json_depth(content)
            indent = min(max(depth, 2), 8)  # keep indent between 2 and 8

            with path.open("w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=indent)

        else:
            # Treat as plain text
            if not isinstance(content, str):
                content = str(content)
            with path.open("w", encoding="utf-8") as f:
                f.write(content)

        document_logger.info(f"✅ Successfully saved content to {path}")
    except Exception as e:
        document_logger.exception(f"❌ Failed to save content to {path}: {e}")

def read_pdf_as_plain(
        file_path: Union[Path, str],
        output_dir: Union[Path, str] = "./",
        start_page: int = None,
        end_page: int = None,

) -> Optional[defaultdict]:
    """
    Reads a PDF safely without executing JavaScript and prints text content.

    Parameters:
        file_path: Path to the PDF file.
        output_dir: dir path to save as JSON
        start_page: 1-based page number to start from (None = start of document).
        end_page: 1-based page number to end at (inclusive) (None = end of document).
    """

    file_path = Path(file_path)

    with fitz.open(file_path) as doc:
        total_pages = len(doc)
        document_logger.info(f"{file_path.suffix[1:].upper()} named {file_path.stem} has {total_pages} pages.")

        # Defaults: full document
        start = (start_page or 1) - 1  # convert to 0-based
        end = end_page or total_pages  # still 1-based here

        # Clamp to valid ranges
        start = max(0, min(start, total_pages - 1))
        end = max(1, min(end, total_pages))

        content = defaultdict(list)
        content["title"] = file_path.stem

        for page_num in range(start, end):
            page = doc[page_num]
            text = page.get_text("text")

            word_count = count_words_in_text(text)

            document_logger.info(f"--- Page {page_num + 1} has {word_count} words ---")
            document_logger.debug(text if text.strip() else "[No extractable text]")

            page_data = {
                "page_num": page_num + 1,
                "content": text,
                "word_count": word_count
            }

            # Append page data to the "pages" list
            content["pages"].append(page_data)

        # Write everything to JSON at once
        output_file = Path(output_dir) / f"{file_path.stem}.json"
        save_content_to_file(content, output_file)

        return content

def main():
    parser = argparse.ArgumentParser(
        prog='ReadPDFasPlainText',
        description='Reads PDF and saves to file'
    )

    parser.add_argument('filename')
    parser.add_argument('output')

    args = parser.parse_args()
    filepath = args.filename

    read_pdf_as_plain(filepath, output_dir=Path(PROJECT_ROOT / "/data/extracted_jsons"))

if __name__ == '__main__':
    main()
