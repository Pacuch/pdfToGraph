from pathlib import Path
from pdf2image import convert_from_path
import numpy as np
from paddleocr import PaddleOCR
from src.logger.document_reader import document_logger
import cv2

# Input / Output paths
INPUT_PDF = Path("../inputs/file.pdf")
OUTPUT_PNG_DIR = Path("../data/extracted_pngs")
OUTPUT_JSON_DIR = Path("../data/extracted_jsons")
DPI = 600
LANG = "en"  # PaddleOCR language code: "en", "ch", "pol", etc.

# Initialize PaddleOCR
ocr = PaddleOCR(
    use_doc_orientation_classify=True, # try to detect document rotation.
    use_doc_unwarping=True, # try to correct warped documents (like scanned pages).
    use_textline_orientation=False # detect individual line orientation.
)

# Convert only the first page of PDF to image
pages = convert_from_path(INPUT_PDF, DPI, first_page=1, last_page=1)

# Process each page with PaddleOCR
for page_number, page_image in enumerate(pages, start=1):
    output_image_path = Path(OUTPUT_PNG_DIR, f"output_page_{page_number}.png")
    output_json_path = Path(OUTPUT_JSON_DIR, f"output_page_{page_number}.json")

    # Save page image
    page_image.save(output_image_path, "PNG")

    # Run OCR
    image_array = cv2.imread(str(output_image_path))
    result = ocr.predict(input=image_array)

    # Save OCR results
    for res in result:
        res.save_to_img(output_image_path)
        res.save_to_json(output_json_path)

    document_logger.info(f"📄 Page {page_number} processed, {len(result)} lines detected")
