from pdf_processor import extract_data_from_pdf
from pathlib import Path

# Test konkrétního PDF z 2025-11-09: Købsrekvisition K0145958 AAL.pdf
pdf_path = Path(
    r'C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky\2025-11-09\Købsrekvisition K0145958 AAL.pdf'
)
print('Loading PDF:', pdf_path)
print('File exists:', pdf_path.exists())

df = extract_data_from_pdf(pdf_path)
print('\n=== EXTRACTION RESULTS ===')
print(f'Rows extracted: {len(df)}')
print(f'Columns: {list(df.columns)}')

if not df.empty:
    print('\n=== FIRST ROW ===')
    first_row = df.iloc[0].to_dict()
    for key, value in first_row.items():
        print(f'{key}: {repr(value)}')

    print('\n=== FULL TABLE ===')
    print(df.to_string(index=False))
