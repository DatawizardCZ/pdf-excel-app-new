import os
import pandas as pd
from pathlib import Path
from pdf_processor import extract_data_from_pdf

def test_all():
    test_dir = Path("test_files")
    if not test_dir.exists():
        print(f"Directory {test_dir} not found!")
        return

    pdf_files = list(test_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in test_files/")
        return

    print(f"Testing {len(pdf_files)} PDF files...")
    print("-" * 60)
    print(f"{'Filename':<40} | {'Rows':<5} | {'Status':<10}")
    print("-" * 60)

    for pdf_file in pdf_files:
        try:
            df = extract_data_from_pdf(pdf_file)
            print(f"{pdf_file.name:<40} | {len(df):<5} | ✅ OK")
        except Exception as e:
            print(f"{pdf_file.name:<40} | {'-':<5} | ❌ Error: {str(e)}")

    print("-" * 60)
    print("Test complete.")

if __name__ == "__main__":
    test_all()
