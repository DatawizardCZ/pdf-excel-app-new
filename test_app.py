"""
Testovací skript pro app.py
Testuje funkce používané v aplikaci bez nutnosti spouštět Streamlit
"""
import sys
from pathlib import Path
import pandas as pd
import io
import tempfile
from pdf_processor import extract_data_from_pdf

def test_pdf_processor():
    """Test PDF procesoru na skutečných PDF souborech"""
    print("=" * 60)
    print("TEST: PDF Processor")
    print("=" * 60)
    
    # Najít všechny PDF soubory v aktuálním adresáři
    pdf_files = list(Path(".").glob("Købsrekvisition*.pdf"))
    
    if not pdf_files:
        print("❌ Nenalezeny žádné PDF soubory k testování")
        print("   Očekávaný formát: Købsrekvisition*.pdf")
        return False
    
    print(f"\nNalezeno {len(pdf_files)} PDF souborů k testování\n")
    
    success_count = 0
    error_count = 0
    
    for pdf_file in pdf_files[:3]:  # Testovat maximálně 3 soubory
        print(f"\n📄 Testování: {pdf_file.name}")
        print("-" * 60)
        
        try:
            # Test extrakce dat
            df = extract_data_from_pdf(pdf_file)
            
            if df.empty:
                print(f"⚠️  Varování: DataFrame je prázdný")
            else:
                print(f"✅ Úspěšně extrahováno {len(df)} řádků")
                print(f"   Sloupce: {', '.join(df.columns)}")
                print(f"   První řádek:")
                print(f"   {df.iloc[0].to_dict()}")
                success_count += 1
            
        except Exception as e:
            print(f"❌ Chyba při zpracování: {str(e)}")
            error_count += 1
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Výsledky: ✅ {success_count} úspěšných, ❌ {error_count} chyb")
    print("=" * 60)
    
    return error_count == 0

def test_excel_generation():
    """Test generování Excel souborů"""
    print("\n" + "=" * 60)
    print("TEST: Excel Generation")
    print("=" * 60)
    
    # Najít jeden PDF soubor
    pdf_files = list(Path(".").glob("Købsrekvisition*.pdf"))
    
    if not pdf_files:
        print("❌ Nenalezeny žádné PDF soubory k testování")
        return False
    
    pdf_file = pdf_files[0]
    print(f"\n📄 Testování s: {pdf_file.name}")
    
    try:
        # Extrahovat data
        df = extract_data_from_pdf(pdf_file)
        
        if df.empty:
            print("⚠️  DataFrame je prázdný, vytvářím testovací data")
            df = pd.DataFrame({
                'Cislo': ['1', '2'],
                'Barcode': ['1234567890', '0987654321'],
                'Popis': ['Test položka 1', 'Test položka 2'],
                'Cena': ['10.50', '20.00']
            })
        
        # Generovat Excel v paměti (stejně jako v app.py)
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Objednávka')
        
        excel_buffer.seek(0)
        excel_data = excel_buffer.getvalue()
        
        print(f"✅ Excel soubor vygenerován v paměti")
        print(f"   Velikost: {len(excel_data)} bajtů")
        print(f"   Počet řádků: {len(df)}")
        
        # Ověřit, že lze načíst zpět
        excel_buffer.seek(0)
        df_read = pd.read_excel(excel_buffer, sheet_name='Objednávka')
        
        if len(df_read) == len(df):
            print(f"✅ Excel soubor lze načíst zpět (validace)")
            return True
        else:
            print(f"❌ Počet řádků se neshoduje: {len(df_read)} vs {len(df)}")
            return False
            
    except Exception as e:
        print(f"❌ Chyba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_file_handling():
    """Test zpracování souborů (simulace uploadu)"""
    print("\n" + "=" * 60)
    print("TEST: File Handling (simulace Streamlit upload)")
    print("=" * 60)
    
    pdf_files = list(Path(".").glob("Købsrekvisition*.pdf"))
    
    if not pdf_files:
        print("❌ Nenalezeny žádné PDF soubory k testování")
        return False
    
    pdf_file = pdf_files[0]
    print(f"\n📄 Simulace uploadu: {pdf_file.name}")
    
    try:
        # Simulace: načtení souboru jako by přišel z Streamlit
        with open(pdf_file, 'rb') as f:
            pdf_bytes = f.read()
        
        print(f"✅ Soubor načten: {len(pdf_bytes)} bajtů")
        
        # Simulace: uložení do dočasného souboru (jako v app.py)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = Path(tmp_file.name)
        
        print(f"✅ Dočasný soubor vytvořen: {tmp_path.name}")
        
        # Zpracování
        df = extract_data_from_pdf(tmp_path)
        print(f"✅ Data extrahována: {len(df)} řádků")
        
        # Smazání dočasného souboru
        if tmp_path.exists():
            tmp_path.unlink()
            print(f"✅ Dočasný soubor smazán")
        
        return True
        
    except Exception as e:
        print(f"❌ Chyba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_files():
    """Test zpracování více souborů najednou"""
    print("\n" + "=" * 60)
    print("TEST: Multiple Files Processing")
    print("=" * 60)
    
    pdf_files = list(Path(".").glob("Købsrekvisition*.pdf"))
    
    if len(pdf_files) < 2:
        print("⚠️  Nalezeno méně než 2 PDF soubory, test přeskočen")
        return True
    
    print(f"\n📄 Testování zpracování {min(3, len(pdf_files))} souborů")
    
    success_count = 0
    error_count = 0
    
    for pdf_file in pdf_files[:3]:
        try:
            df = extract_data_from_pdf(pdf_file)
            if not df.empty:
                success_count += 1
                print(f"✅ {pdf_file.name}: {len(df)} řádků")
            else:
                print(f"⚠️  {pdf_file.name}: prázdný DataFrame")
        except Exception as e:
            error_count += 1
            print(f"❌ {pdf_file.name}: {str(e)}")
    
    print(f"\nVýsledky: ✅ {success_count} úspěšných, ❌ {error_count} chyb")
    return error_count == 0

def run_all_tests():
    """Spustit všechny testy"""
    print("\n" + "=" * 60)
    print("SPOUŠTĚNÍ VŠECH TESŤŮ")
    print("=" * 60)
    
    results = []
    
    # Spustit jednotlivé testy
    results.append(("PDF Processor", test_pdf_processor()))
    results.append(("Excel Generation", test_excel_generation()))
    results.append(("File Handling", test_file_handling()))
    results.append(("Multiple Files", test_multiple_files()))
    
    # Shrnutí
    print("\n" + "=" * 60)
    print("SHRNUTÍ TESŤŮ")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ VŠECHNY TESTY PROŠLY")
    else:
        print("❌ NĚKTERÉ TESTY SELHALY")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest přerušen uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Neočekávaná chyba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




