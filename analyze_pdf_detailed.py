"""
Detailní analýza PDF - extrakce strukturovaných dat z textu
"""

import pdfplumber
from pathlib import Path
import re

def extract_table_from_text(text):
    """Extrahuje tabulku z textu podle struktury"""
    
    # Hledání hlavičky tabulky
    # Možné varianty: "No. Barcode No. Description..." nebo dánské ekvivalenty
    header_patterns = [
        r'No\.\s+Barcode\s+No\.\s+Description',  # Anglická hlavička
        r'Nr\.\s+Stregkode\s+Nr\.\s+Beskrivelse',  # Dánská hlavička
    ]
    
    lines = text.split('\n')
    
    # Najít řádek s hlavičkou tabulky (řádek s "No. Barcode No. Description...")
    header_line_idx = None
    header_line = None
    
    for i, line in enumerate(lines):
        for pattern in header_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                header_line_idx = i
                header_line = line
                break
        if header_line_idx is not None:
            break
    
    if header_line_idx is None:
        print("Hlavička tabulky nenalezena!")
        # Zkusit najít alespoň řádek s "Vendor Item Cost" a pak hledat hlavičku na dalším řádku
        for i, line in enumerate(lines):
            if 'Vendor Item Cost' in line and i + 1 < len(lines):
                # Další řádek by měl být hlavička
                next_line = lines[i + 1].strip()
                if 'No.' in next_line or 'Nr.' in next_line:
                    header_line_idx = i + 1
                    header_line = next_line
                    break
        
        if header_line_idx is None:
            print("Hlavička tabulky nenalezena ani po druhém pokusu!")
            return None
    
    print(f"Nalezena hlavička na řádku {header_line_idx + 1}:")
    print(f"  {header_line}\n")
    
    # Extrahovat hlavičky
    headers = re.split(r'\s{2,}', header_line.strip())  # Rozdělení podle více mezer
    headers = [h.strip() for h in headers if h.strip()]
    
    print(f"Rozpoznané hlavičky ({len(headers)}):")
    for i, h in enumerate(headers, 1):
        print(f"  {i}. '{h}'")
    print()
    
    # Najít data řádky (řádky po hlavičce, které vypadají jako data)
    data_rows = []
    
    for i in range(header_line_idx + 1, len(lines)):
        line = lines[i].strip()
        
        # Přeskočit prázdné řádky
        if not line:
            continue
        
        # Přeskočit řádky, které jsou součástí hlavičky nebo patičky
        if any(keyword in line.lower() for keyword in ['total', 'sum', 'i alt', 'side', 'page']):
            continue
        
        # Zkontrolovat, jestli řádek vypadá jako datový řádek
        # Datový řádek obvykle začíná číslem (číslo položky) nebo čárovým kódem
        # a obsahuje čísla (ceny, množství)
        
        # Rozdělit řádek podle více mezer nebo tabulátorů
        row_data = re.split(r'\s{2,}|\t', line)
        row_data = [d.strip() for d in row_data if d.strip()]
        
        # Datový řádek by měl:
        # 1. Začínat číslem nebo čárovým kódem (dlouhé číslo)
        # 2. Obsahovat alespoň 3 sloupce
        # 3. Obsahovat čísla (ceny, množství)
        if len(row_data) >= 3:
            # Zkontrolovat, jestli první sloupec je číslo nebo čárový kód
            first_col = row_data[0]
            if (first_col.isdigit() or 
                (len(first_col) > 10 and first_col.replace('.', '').isdigit()) or  # Čárový kód
                re.match(r'^\d+$', first_col)):  # Číslo
                
                # Zkontrolovat, jestli řádek obsahuje čísla (ceny, množství)
                has_numbers = any(re.search(r'\d+[.,]\d+|\d+', col) for col in row_data[2:])
                
                if has_numbers:
                    data_rows.append(row_data)
                    print(f"Datový řádek {len(data_rows)}: {row_data}")
    
    print(f"\nNalezeno {len(data_rows)} datových řádků\n")
    
    return {
        'headers': headers,
        'data_rows': data_rows
    }

def analyze_pdf_detailed(pdf_path):
    """Detailní analýza jednoho PDF"""
    print(f"\n{'='*80}")
    print(f"Detailní analýza: {pdf_path.name}")
    print(f"{'='*80}\n")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Zkombinovat text ze všech stránek
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Zobrazit celý text (pro debug)
        print("=== CELÝ TEXT Z PDF ===")
        print(full_text[:2000])  # Prvních 2000 znaků
        print("\n" + "="*80 + "\n")
        
        # Extrahovat tabulku
        table_data = extract_table_from_text(full_text)
        
        return table_data

def main():
    """Hlavní funkce"""
    pdf_dir = Path(__file__).parent
    
    # Analyzovat první PDF pro začátek
    pdf_file = pdf_dir / "Købsrekvisition K0145920 EGA.pdf"
    
    if not pdf_file.exists():
        print(f"Soubor {pdf_file} neexistuje!")
        return
    
    analyze_pdf_detailed(pdf_file)

if __name__ == "__main__":
    main()

