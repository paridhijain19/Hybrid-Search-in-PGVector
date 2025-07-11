#code 2
import fitz  # PyMuPDF
import os
print(fitz.__doc__)
DATA_DIR = "data"
OUTPUT_DIR = "processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".pdf"):
        input_path = os.path.join(DATA_DIR, filename)
        text = extract_text_from_pdf(input_path)

        output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".txt"))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted: {filename}")
