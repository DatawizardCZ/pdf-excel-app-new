"""
Skript pro analýzu struktury PDF souborů
Pomáhá zjistit, jak jsou data strukturovaná v PDF
"""

import pdfplumber
from pathlib import Path
import json

def analyze_pdf(pdf_path):
    """Analyzuje strukturu PDF souboru"""
    print(f"\n{'='*80}")
    print(f"Analyzuji: {pdf_path.name}")
    print(f"{'='*80}\n")
    
    results = {
        'file': pdf_path.name,
        'pages': [],
        'tables_found': 0,
        'text_samples': []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Počet stránek: {len(pdf.pages)}\n")
        
        for i, page in enumerate(pdf.pages, 1):
            print(f"--- Stránka {i} ---")
            
            # Extrakce textu
            text = page.extract_text()
            if text:
                lines = text.split('\n')[:20]  # Prvních 20 řádků
                print("Prvních 20 řádků textu:")
                for line in lines:
                    if line.strip():
                        print(f"  {line}")
                print()
            
            # Hledání tabulek
            tables = page.extract_tables()
            if tables:
                print(f"Nalezeno tabulek: {len(tables)}\n")
                results['tables_found'] += len(tables)
                
                for j, table in enumerate(tables, 1):
                    print(f"Tabulka {j}:")
                    print(f"  Počet řádků: {len(table)}")
                    print(f"  Počet sloupců: {len(table[0]) if table else 0}")
                    
                    # Zobrazení prvních řádků
                    print("  První řádky tabulky:")
                    for row_idx, row in enumerate(table[:5], 1):
                        print(f"    Řádek {row_idx}: {row}")
                    print()
                    
                    # Uložení struktury tabulky
                    page_info = {
                        'page': i,
                        'table': j,
                        'rows': len(table),
                        'cols': len(table[0]) if table else 0,
                        'header': table[0] if table else None,
                        'first_data_row': table[1] if len(table) > 1 else None,
                        'sample_rows': table[:3] if len(table) >= 3 else table
                    }
                    results['pages'].append(page_info)
            else:
                print("Žádné tabulky nenalezeny\n")
            
            # Hledání textových objektů
            words = page.extract_words()
            if words:
                print(f"Počet slov na stránce: {len(words)}")
                print("Prvních 10 slov:")
                for word in words[:10]:
                    print(f"  '{word['text']}' na pozici ({word['x0']:.1f}, {word['top']:.1f})")
                print()
    
    return results

def main():
    """Hlavní funkce pro analýzu všech PDF souborů"""
    pdf_dir = Path(__file__).parent
    
    # Najít všechny PDF soubory
    pdf_files = list(pdf_dir.glob("Købsrekvisition*.pdf"))
    
    if not pdf_files:
        print("Nenalezeny žádné PDF soubory!")
        return
    
    print(f"Nalezeno {len(pdf_files)} PDF souborů\n")
    
    all_results = []
    
    # Analyzovat každý PDF
    for pdf_file in pdf_files[:3]:  # Pro začátek analyzujeme první 3
        try:
            results = analyze_pdf(pdf_file)
            all_results.append(results)
        except Exception as e:
            print(f"Chyba při analýze {pdf_file.name}: {e}\n")
    
    # Uložit výsledky do JSON
    output_file = pdf_dir / "pdf_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"Analýza dokončena! Výsledky uloženy do: {output_file.name}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

