"""
Modul pro zpracování PDF objednávek
Extrahuje data z PDF a transformuje je do strukturovaného formátu
"""

import pdfplumber
import pandas as pd
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Ponecháme původní názvy sloupců z PDF - žádné mapování na české názvy
# Specifikace (druhý řádek popisu) zůstane v samostatném sloupci "Specification"


def detect_language(headers: List[str]) -> str:
    """Detekuje jazyk headerů (dánsky/anglicky)"""
    danish_keywords = ['Nr.', 'Stregkode', 'Beskrivelse', 'Pris', 'Antal', 'Styk']
    
    headers_text = ' '.join(headers).lower()
    danish_count = sum(1 for keyword in danish_keywords if keyword.lower() in headers_text)
    
    return 'danish' if danish_count > 2 else 'english'


def parse_header_line(header_line: str) -> List[str]:
    """Parsuje řádek s hlavičkou do jednotlivých sloupců - zachová původní názvy 1:1"""
    # Hlavička může být např.: "Vendor Item No. Barcode No. Description Variant Cost Price Quantity Kolli Str. Pieces"
    # Sloupce jsou odděleny více mezerami (2+ mezery)
    
    # Nejdříve zkusit rozdělit podle více mezer (2+ mezery = oddělovač sloupců)
    # Toto je nejspolehlivější metoda pro PDF tabulky
    headers = re.split(r'\s{2,}', header_line.strip())
    headers = [h.strip() for h in headers if h.strip()]
    
    # Pokud jsme dostali rozumný počet sloupců (alespoň 5), použít to
    if len(headers) >= 5:
        # Vyčistit - zajistit, že "Kolli Str." není rozděleno a odstranit samostatné "No."
        cleaned_headers = []
        i = 0
        while i < len(headers):
            header = headers[i].strip()
            if not header:
                i += 1
                continue
            
            # Spojit "Vendor Item No." pokud je rozděleno (různé kombinace)
            if (cleaned_headers and len(cleaned_headers) >= 2 and 
                cleaned_headers[-2].lower() == 'vendor' and 
                cleaned_headers[-1].lower() == 'item' and 
                header in ['No.', 'Nr.']):
                cleaned_headers[-2] = 'Vendor Item ' + header
                cleaned_headers.pop()
                i += 1
            # Spojit "Vendor" a "Item" pokud jsou rozděleny
            elif header.lower() == 'item' and cleaned_headers and cleaned_headers[-1].lower() == 'vendor':
                cleaned_headers[-1] = 'Vendor Item'
                i += 1
            # Spojit "Vendor Item" s "No." pokud následuje
            elif header in ['No.', 'Nr.'] and cleaned_headers and cleaned_headers[-1].lower() == 'vendor item':
                cleaned_headers[-1] = cleaned_headers[-1] + ' ' + header
                i += 1
            # Spojit "Vendor Item No." pokud je rozděleno na tři části (Vendor, Item, No.)
            elif (header in ['No.', 'Nr.'] and 
                  cleaned_headers and len(cleaned_headers) >= 2 and
                  'vendor' in cleaned_headers[-2].lower() and 
                  'item' in cleaned_headers[-1].lower()):
                # Spojit všechny tři části
                combined = cleaned_headers[-2] + ' ' + cleaned_headers[-1] + ' ' + header
                cleaned_headers[-2] = combined
                cleaned_headers.pop()
                i += 1
            # Spojit "Cost" a "Price" do "Cost Price"
            elif header == 'Cost' and i + 1 < len(headers) and headers[i + 1].strip().lower() == 'price':
                cleaned_headers.append('Cost Price')
                i += 2
            elif header.lower() == 'price' and i > 0 and cleaned_headers and cleaned_headers[-1].lower() == 'cost':
                # Nahradit předchozí "Cost" za "Cost Price"
                cleaned_headers[-1] = 'Cost Price'
                i += 1
            # Spojit "Kolli" a "Str." do "Kolli Str."
            elif header == 'Kolli' and i + 1 < len(headers) and headers[i + 1].strip() == 'Str.':
                cleaned_headers.append('Kolli Str.')
                i += 2
            elif header == 'Str.' and i > 0 and cleaned_headers and cleaned_headers[-1] == 'Kolli':
                # Nahradit předchozí "Kolli" za "Kolli Str."
                cleaned_headers[-1] = 'Kolli Str.'
                i += 1
            elif header in ['No.', 'Nr.']:
                # Spojit s předchozí hlavičkou pokud je to "Barcode" nebo "Stregkode"
                if (cleaned_headers and 
                    (cleaned_headers[-1].lower() in ['barcode', 'stregkode'])):
                    cleaned_headers[-1] = cleaned_headers[-1] + ' ' + header
                # Jinak přeskočit - není to platná samostatná hlavička
                i += 1
            else:
                cleaned_headers.append(header)
                i += 1
        
        # Odstranit duplikáty při zachování pořadí
        seen = set()
        final_headers = []
        for header in cleaned_headers:
            if header not in seen:
                seen.add(header)
                final_headers.append(header)
        
        return final_headers
    
    # Pokud ne, zkusit inteligentnější parsování s pattern matching
    # Pro víceslovné hlavičky jako "Vendor Item No.", "Barcode No.", "Cost Price", "Kolli Str."
    # DŮLEŽITÉ: Víceslovné hlavičky MUSÍ být před jednoslovnými, aby se "No." nespárovalo samostatně
    header_patterns = [
        # Víceslovné hlavičky (MUSÍ být před jednoslovnými!)
        (r'Vendor\s+Item\s+No\.', 'Vendor Item No.'),
        (r'Barcode\s+No\.', 'Barcode No.'),
        (r'Cost\s+Price', 'Cost Price'),
        (r'Kolli\s+Str\.', 'Kolli Str.'),
        (r'Stregkode\s+Nr\.', 'Stregkode Nr.'),  # Dánská varianta
        # Jednoslovné hlavičky (pouze pokud nejsou součástí víceslovných)
        (r'\bDescription\b', 'Description'),
        (r'\bBeskrivelse\b', 'Beskrivelse'),  # Dánská varianta
        (r'\bVariant\b', 'Variant'),
        (r'\bQuantity\b', 'Quantity'),
        (r'\bAntal\b', 'Antal'),  # Dánská varianta
        (r'\bPrice\b', 'Price'),  # Pouze pokud není "Cost Price"
        (r'\bPris\b', 'Pris'),  # Dánská varianta
        (r'\bPieces\b', 'Pieces'),
        (r'\bStyk\b', 'Styk'),  # Dánská varianta
    ]
    
    headers = []
    remaining = header_line
    used_positions = set()
    
    # Najít všechny hlavičky v pořadí (pouze víceslovné nejdříve)
    matches = []
    for pattern, header_name in header_patterns:
        for match in re.finditer(pattern, remaining, re.IGNORECASE):
            start, end = match.span()
            # Zkontrolovat, jestli tato pozice už není použita
            if not any(start <= pos < end for pos in used_positions):
                matches.append((start, end, header_name))
                # Označit pozice jako použité
                for pos in range(start, end):
                    used_positions.add(pos)
    
    # Seřadit podle pozice
    matches.sort(key=lambda x: x[0])
    
    # Sestavit seznam hlaviček v pořadí
    for start, end, header_name in matches:
        headers.append(header_name)
    
    # Pokud jsme nenašli žádné hlavičky, zkusit jednodušší rozdělení
    if not headers:
        headers = re.split(r'\s+', header_line.strip())
        headers = [h.strip() for h in headers if h.strip()]
    
    # Vyčistit - odstranit prázdné a zajistit správné názvy
    cleaned_headers = []
    i = 0
    while i < len(headers):
        header = headers[i].strip()
        if not header:
            i += 1
            continue
        
        # Zkontrolovat, jestli není "Kolli Str." rozděleno
        if header == 'Kolli' and i + 1 < len(headers) and headers[i + 1].strip() == 'Str.':
            cleaned_headers.append('Kolli Str.')
            i += 2
        elif header == 'Str.' and i > 0 and cleaned_headers and cleaned_headers[-1] == 'Kolli':
            # Nahradit předchozí "Kolli" za "Kolli Str."
            cleaned_headers[-1] = 'Kolli Str.'
            i += 1
        elif header in ['No.', 'Nr.']:
            # Přeskočit samostatné "No." nebo "Nr." - měly by být pouze součástí "Vendor Item No." nebo "Barcode No."
            # Pokud předchozí hlavička není "Vendor Item" nebo "Barcode", přeskočit
            if (cleaned_headers and 
                (cleaned_headers[-1].lower() in ['vendor item', 'barcode', 'stregkode'])):
                # Spojit s předchozí hlavičkou
                cleaned_headers[-1] = cleaned_headers[-1] + ' ' + header
            # Jinak přeskočit - není to platná samostatná hlavička
            i += 1
        else:
            cleaned_headers.append(header)
            i += 1
    
    # Odstranit duplikáty při zachování pořadí
    seen = set()
    final_headers = []
    for header in cleaned_headers:
        if header not in seen:
            seen.add(header)
            final_headers.append(header)
    
    return final_headers


def extract_data_from_pdf(pdf_path: Path) -> pd.DataFrame:
    """
    Extrahuje data z PDF souboru a vrátí DataFrame
    
    Args:
        pdf_path: Cesta k PDF souboru
        
    Returns:
        DataFrame se strukturovanými daty
    """
    all_rows = []
    current_item = None
    
    with pdfplumber.open(pdf_path) as pdf:
        # Zkombinovat text ze všech stránek
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        lines = full_text.split('\n')
        
        # Najít hlavičku tabulky
        header_line_idx = None
        header_line = None
        
        # Hledat řádek s hlavičkou - různé varianty
        # Prioritně hledat "Vendor Item No." jako první sloupec
        for i, line in enumerate(lines):
            # Hledat "Vendor Item No." jako první indikátor
            if re.search(r'Vendor\s+Item\s+No\.', line, re.IGNORECASE):
                header_line_idx = i
                header_line = line
                break
            # Pak hledat "Barcode No." nebo dánskou variantu
            elif (re.search(r'No\.\s+Barcode|Nr\.\s+Stregkode', line, re.IGNORECASE) or
                  re.search(r'Barcode\s+No\.', line, re.IGNORECASE)):
                header_line_idx = i
                header_line = line
                break
        
        # Pokud nenalezeno, zkusit najít "Vendor Item Cost" a pak hlavičku
        if header_line_idx is None:
            for i, line in enumerate(lines):
                if 'Vendor Item Cost' in line and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if 'No.' in next_line or 'Nr.' in next_line or 'Vendor Item' in next_line:
                        header_line_idx = i + 1
                        header_line = next_line
                        break
        
        if header_line_idx is None:
            raise ValueError("Hlavička tabulky nenalezena v PDF!")
        
        # Parsovat hlavičku - ponecháme původní názvy z PDF
        headers = parse_header_line(header_line)
        
        # Vyčistit názvy hlaviček (odstranit přebytečné mezery)
        cleaned_headers = [h.strip() for h in headers if h.strip()]
        
        # Zajistit, že "Vendor Item No." je první sloupec
        # Zkontrolovat, jestli už existuje
        has_vendor_item_no = any('vendor' in h.lower() and 'item' in h.lower() for h in cleaned_headers)
        
        if not has_vendor_item_no:
            # Přidat "Vendor Item No." jako první sloupec
            cleaned_headers.insert(0, 'Vendor Item No.')
        
        # Použít původní názvy z PDF (bez mapování)
        original_headers = cleaned_headers
        
        # Extrahovat data řádky
        data_start = header_line_idx + 1
        
        for i in range(data_start, len(lines)):
            line = lines[i].strip()
            
            # Přeskočit prázdné řádky
            if not line:
                continue
            
            # Přeskočit patičku
            if any(keyword in line.lower() for keyword in ['total', 'sum', 'i alt', 'page']):
                break
            
            # Zkontrolovat, jestli je to víceřádková položka (druhý řádek - specifikace)
            # Druhý řádek obvykle nezačíná číslem a je pod datovým řádkem
            # Také nesmí být prázdný řádek nebo patička
            if (current_item is not None and 
                not re.match(r'^\d+', line) and 
                line.strip() and
                not any(keyword in line.lower() for keyword in ['total', 'sum', 'i alt', 'page', 'side'])):
                # Toto je specifikace (druhý řádek popisu) - uložit do samostatného sloupce
                current_item['Specification'] = line.strip()
                all_rows.append(current_item.copy())
                current_item = None
                continue
            
            # Datový řádek by měl začínat číslem (Vendor Item No.)
            if not re.match(r'^\d+', line):
                continue
            
            # Pokud máme aktuální položku a narazíme na nový datový řádek,
            # musíme nejdříve přidat předchozí položku (neměla specifikaci)
            if current_item is not None:
                all_rows.append(current_item.copy())
                current_item = None
            
            # Rozdělit řádek na části
            parts = line.split()
            
            if len(parts) < 5:
                continue
            
            row_data = []
            
            # 1. Vendor Item No. - první část
            #    Původně bylo očekáváno čistě číselné ID (např. 159105).
            #    Nyní podporujeme i 6místné alfanumerické kódy, kde poslední znak může být písmeno,
            #    např. 15910S.
            vendor_item_token = parts[0]
            if re.match(r'^\d{5}[A-Za-z0-9]?$', vendor_item_token):
                row_data.append(vendor_item_token)
                parts = parts[1:]
            else:
                # Pokud první token neodpovídá očekávanému formátu Vendor Item, přeskočíme řádek
                continue
            
            # 2. Barcode No. - druhá část (dlouhé číslo, typicky 13 cifer)
            if parts and parts[0].isdigit() and len(parts[0]) >= 10:
                row_data.append(parts[0])
                parts = parts[1:]
            else:
                continue
            
            remaining = ' '.join(parts)
            
            # 3-4. Description a Variant (Variant bývá prázdný)
            # Najít první hodnotu, která vypadá jako cena - musí obsahovat desetinnou čárku nebo tečku
            price_match = re.search(r'\d+(?:[.,]\d{2})', remaining)
            if not price_match:
                # Pokud nenajdeme cenu s desetinnou čárkou, řádek nemá očekávanou strukturu
                continue
            
            description_text = remaining[:price_match.start()].strip()
            price_value = price_match.group(0)
            after_price = remaining[price_match.end():].strip()
            
            # Po ceně následují tři číselné sloupce: Quantity, Kolli Str., Pieces
            trailing_tokens = re.split(r'\s+', after_price)
            trailing_tokens = [token.strip() for token in trailing_tokens if token.strip()]
            
            quantity = trailing_tokens[0] if len(trailing_tokens) > 0 else ''
            kolli = trailing_tokens[1] if len(trailing_tokens) > 1 else ''
            pieces = trailing_tokens[2] if len(trailing_tokens) > 2 else ''
            
            # Pokud description obsahuje více řádků (oddělené mezerami nebo skutečnými newlines),
            # rozdělit na první řádek (Description) a zbytek (půjde do Specification později)
            # Ale pro teď uložit celý text do Description - Specification se přidá z následujícího řádku
            row_data.append(description_text)
            row_data.append('')  # Variant
            row_data.append(price_value)
            row_data.append(quantity)
            row_data.append(kolli)
            row_data.append(pieces)
            
            # Datový řádek by měl obsahovat alespoň 3 sloupce
            if len(row_data) >= 3:
                # Vytvořit slovník pro tento řádek
                item = {}
                
                # Explicitně mapovat hodnoty na správné sloupce podle jejich názvů
                # Struktura row_data: [Vendor Item No., Barcode No., Description, Variant, Cost Price, Quantity, Kolli Str., Pieces]
                vendor_item_no = row_data[0] if len(row_data) > 0 else ''
                barcode_no = row_data[1] if len(row_data) > 1 else ''
                description = row_data[2] if len(row_data) > 2 else ''
                variant = row_data[3] if len(row_data) > 3 else ''
                cost_price = row_data[4] if len(row_data) > 4 else ''
                quantity = row_data[5] if len(row_data) > 5 else ''
                kolli_str = row_data[6] if len(row_data) > 6 else ''
                pieces = row_data[7] if len(row_data) > 7 else ''
                
                # Mapovat na správné názvy sloupců z PDF (podporovat anglické i dánské názvy)
                # DŮLEŽITÉ: Kontrolovat nejdříve víceslovné názvy, pak jednoslovné
                # Nejdříve explicitně najít "Vendor Item No." sloupec
                vendor_item_col = None
                for col_name in original_headers:
                    col_lower = col_name.lower().strip()
                    if 'vendor' in col_lower and 'item' in col_lower:
                        vendor_item_col = col_name
                        break
                
                # Mapovat všechny sloupce
                for col_name in original_headers:
                    col_lower = col_name.lower().strip()
                    
                    # Víceslovné hlavičky (nejdříve!) - musí být přesné matchování
                    # "Vendor Item No." - explicitně přiřadit vendor_item_no
                    if col_name == vendor_item_col or ('vendor' in col_lower and 'item' in col_lower):
                        item[col_name] = vendor_item_no
                    elif ('barcode' in col_lower or 'stregkode' in col_lower) and ('no' in col_lower or 'nr' in col_lower):
                        item[col_name] = barcode_no
                    elif 'cost' in col_lower and 'price' in col_lower:
                        item[col_name] = cost_price
                    elif 'kolli' in col_lower and 'str' in col_lower:
                        item[col_name] = kolli_str
                    # Jednoslovné hlavičky
                    elif col_lower in ['description', 'beskrivelse']:
                        item[col_name] = description
                    elif col_lower == 'variant':
                        item[col_name] = variant
                    elif col_lower in ['quantity', 'antal']:
                        item[col_name] = quantity
                    elif col_lower in ['pieces', 'styk']:
                        item[col_name] = pieces
                    elif col_lower == 'price' and 'cost' not in col_lower:
                        # Pouze "Price" (ne "Cost Price") - použít cost_price
                        item[col_name] = cost_price
                    elif col_lower == 'pris':
                        item[col_name] = cost_price
                    elif col_lower in ['no.', 'nr.'] and 'vendor' not in col_lower and 'barcode' not in col_lower:
                        # Samostatné "No." nebo "Nr." - může to být Vendor Item No. pokud není správně parsováno
                        # Zkusit zkontrolovat, jestli předchozí sloupec není "Vendor Item"
                        item[col_name] = ''  # Nechat prázdné, nebo zkusit přiřadit vendor_item_no?
                    else:
                        # Pro neznámé sloupce použít prázdný string
                        item[col_name] = ''
                
                # Fallback: Pokud "Vendor Item No." nebyl namapován, zkusit najít první sloupec s "vendor" nebo "item"
                # nebo první sloupec vůbec a přiřadit vendor_item_no
                vendor_mapped = any('vendor' in col.lower() and 'item' in col.lower() and item.get(col) == vendor_item_no 
                                   for col in original_headers)
                if not vendor_mapped and vendor_item_no:
                    # Najít první sloupec, který obsahuje "vendor", "item", nebo "no" a není namapován
                    found = False
                    for col_name in original_headers:
                        col_lower = col_name.lower().strip()
                        if (('vendor' in col_lower or 'item' in col_lower or 'no' in col_lower or 'nr' in col_lower) 
                            and not item.get(col_name)):
                            item[col_name] = vendor_item_no
                            found = True
                            break
                    # Pokud stále není namapováno, použít první sloupec
                    if not found and original_headers and not item.get(original_headers[0]):
                        item[original_headers[0]] = vendor_item_no
                
                # Přidat sloupec pro specifikaci (pokud bude)
                if 'Specification' not in item:
                    item['Specification'] = ''
                
                # Uložit jako aktuální položku (může následovat řádek se specifikací)
                current_item = item
                # NEPŘIDÁVAT hned - počkat, jestli není další řádek se specifikací
        
        # Přidat poslední položku, pokud existuje (a nebyla přidána s upřesněním)
        if current_item:
            all_rows.append(current_item)
    
    # Vytvořit DataFrame s původními názvy sloupců z PDF
    if not all_rows:
        # Pokud nejsou žádná data, použít hlavičky z PDF + Specification
        if original_headers:
            columns = original_headers + ['Specification']
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.DataFrame()
    else:
        df = pd.DataFrame(all_rows)
        
        # Zajistit, že všechny sloupce z PDF existují
        for col in original_headers:
            if col not in df.columns:
                df[col] = ''
        
        # Zajistit, že sloupec Specification existuje
        if 'Specification' not in df.columns:
            df['Specification'] = ''
        
        # Seřadit sloupce: nejprve původní z PDF, pak Specification
        # Zajistit, že "Vendor Item No." je první (pokud existuje)
        column_order = original_headers + ['Specification']
        
        # Explicitně zajistit, že "Vendor Item No." je první
        vendor_item_cols = [col for col in column_order if 'vendor' in col.lower() and 'item' in col.lower()]
        if vendor_item_cols:
            # Odstranit z původního pořadí a přidat na začátek
            column_order = [vendor_item_cols[0]] + [col for col in column_order if col != vendor_item_cols[0]]
        
        # Použít pouze sloupce, které skutečně existují v DataFrame
        existing_columns = [col for col in column_order if col in df.columns]
        # Přidat případné další sloupce, které nejsou v pořadí
        other_columns = [col for col in df.columns if col not in existing_columns]
        df = df[existing_columns + other_columns]
    
    return df


def process_pdf_to_excel(pdf_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Zpracuje PDF soubor a vytvoří Excel soubor
    
    Args:
        pdf_path: Cesta k PDF souboru
        output_path: Cesta k výstupnímu Excel souboru (pokud None, použije název PDF)
        
    Returns:
        Cesta k vytvořenému Excel souboru
    """
    if output_path is None:
        output_path = pdf_path.parent / f"{pdf_path.stem}_processed.xlsx"
    
    # Extrahovat data
    df = extract_data_from_pdf(pdf_path)
    
    # Uložit do Excelu
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Objednávka')
    
    return output_path

