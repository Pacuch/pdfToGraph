import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from src.logger.document_reader import document_logger

INPUT_PDF = Path("../inputs/file.pdf")
OUTPUT_TXT = Path("../loaded_data/output.txt")
DPI = 600
LANG = "pol"

def write_numbered_lines(path: Path, lines):
    """Write numbered lines to file at 'path'."""
    try:
        width = len(str(len(lines)))
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            for idx, line in enumerate(lines, start=1):
                f.write(f"{idx:0{width}d}: {line.rstrip()}\n")

        document_logger.info(f"✅ {len(lines)} lines written successfully to {path.resolve()}")
    except FileNotFoundError:
        document_logger.error(f"❌ Directory not found: {path.parent}")
    except PermissionError:
        document_logger.error(f"❌ Permission denied when writing to: {path}")
    except Exception as e:
        document_logger.error(f"❌ An unexpected error occurred: {e}")

# Convert PDF to images
pages = convert_from_path(INPUT_PDF, DPI)

# Extract text from each page
full_text = "\n".join(
    pytesseract.image_to_string(page, lang=LANG) for page in pages
)

lines = full_text.splitlines()

# Write numbered lines to file
write_numbered_lines(OUTPUT_TXT, lines)
