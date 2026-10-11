import os
import pandas as pd
import fitz  # or: import pymupdf as fitz
from docx import Document

class ContentExtractor:
    def __init__(self, directory=None):
        if directory is None:
            # Resolves AI Slide generator/data regardless of where you run the script from
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
            self.directory = base_dir
        else:
            self.directory = directory

    def extract_text_from_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def extract_text_from_pdf(self, file_path):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
        return text

    def extract_text_from_docx(self, file_path):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def extract_text_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        return df.to_string()

    def extract_from_file(self, file_path):
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == ".txt":
            return self.extract_text_from_txt(file_path)
        elif ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return self.extract_text_from_docx(file_path)
        elif ext == ".csv":
            return self.extract_text_from_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def extract_from_directory(self):
        extracted_data = {}
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"Directory not found: {self.directory}")

        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path):
                try:
                    extracted_data[filename] = self.extract_from_file(file_path)
                except Exception as e:
                    print(f"Error Processing {filename}: {e}")

        return extracted_data


if __name__ == "__main__":
    extractor = ContentExtractor()
    extracted_content = extractor.extract_from_directory()

    for file, content in extracted_content.items():
        print(f"\nExtracted content from {file}:\n{content[:500]}....\n")