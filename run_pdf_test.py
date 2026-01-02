from pathlib import Path
import sys

import pdf_processor as p


def main() -> None:
    """
    Simple helper script to run pdf_processor.extract_data_from_pdf
    and print the resulting DataFrame as a markdown table.
    """
    if len(sys.argv) < 2:
        print("Usage: python run_pdf_test.py <pdf_path>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"PDF file not found: {pdf_path}")
        sys.exit(1)

    df = p.extract_data_from_pdf(pdf_path)

    try:
        # pandas >= 1.0 has to_markdown; if not available, fall back to to_string
        print(df.to_markdown(index=False))
    except Exception:
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()








