"""Test PDF procesoru"""

from pathlib import Path
from pdf_processor import extract_data_from_pdf, process_pdf_to_excel

# Test na jednom PDF
pdf_file = Path("Købsrekvisition K0145920 EGA.pdf")

if pdf_file.exists():
    print(f"Testuji zpracování: {pdf_file.name}\n")
    
    try:
        # Extrahovat data
        df = extract_data_from_pdf(pdf_file)
        
        print(f"Extrahováno {len(df)} řádků")
        print(f"\nSloupce: {list(df.columns)}")
        print(f"\nPrvních 5 řádků:")
        print(df.head().to_string())
        
        # Zpracovat do Excelu
        excel_file = process_pdf_to_excel(pdf_file)
        print(f"\n✅ Excel soubor vytvořen: {excel_file}")
        
    except Exception as e:
        print(f"❌ Chyba: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"Soubor {pdf_file} neexistuje!")

