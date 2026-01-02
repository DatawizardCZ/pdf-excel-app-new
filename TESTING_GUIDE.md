# 🧪 Průvodce testováním aplikace

Tento dokument popisuje různé způsoby testování `app.py`.

## 📋 Obsah

1. [Rychlé testování](#rychl%C3%A9-testov%C3%A1n%C3%AD)
2. [Automatické testy](#automatick%C3%A9-testy)
3. [Manuální testování](#manu%C3%A1ln%C3%AD-testov%C3%A1n%C3%AD)
4. [Testování v prohlížeči](#testov%C3%A1n%C3%AD-v-prohl%C3%AD%C5%BE%C4%8D%C3%AD)

---

## Rychlé testování

### 1. Spuštění automatických testů

```bash
python test_app.py
```

Tento skript testuje:
- ✅ Zpracování PDF souborů
- ✅ Generování Excel souborů
- ✅ Zpracování souborů (simulace uploadu)
- ✅ Zpracování více souborů najednou

### 2. Test PDF procesoru

```bash
python test_processor.py
```

Testuje zpracování jednoho konkrétního PDF souboru.

---

## Automatické testy

### Spuštění všech testů

```bash
# Windows
python test_app.py

# Linux/Mac
python3 test_app.py
```

### Co testy kontrolují:

1. **PDF Processor Test**
   - Najde všechny PDF soubory v adresáři
   - Otestuje extrakci dat z každého PDF
   - Ověří strukturu výsledného DataFrame

2. **Excel Generation Test**
   - Testuje generování Excel souborů v paměti
   - Ověří, že Excel lze načíst zpět
   - Kontroluje správnost dat

3. **File Handling Test**
   - Simuluje upload souboru (jako v Streamlit)
   - Testuje vytváření a mazání dočasných souborů
   - Ověří celý proces zpracování

4. **Multiple Files Test**
   - Testuje zpracování více souborů najednou
   - Ověří, že každý soubor je zpracován správně

---

## Manuální testování

### 1. Spuštění aplikace

```bash
streamlit run app.py
```

Aplikace se otevře na: `http://localhost:8501`

### 2. Testovací scénáře

#### Scénář 1: Základní test
1. ✅ Otevřete aplikaci v prohlížeči
2. ✅ Nahrajte jeden PDF soubor
3. ✅ Klikněte na "Zpracovat objednávky"
4. ✅ Ověřte, že se zobrazí tlačítko pro stažení Excelu
5. ✅ Stáhněte Excel a ověřte obsah

#### Scénář 2: Více souborů
1. ✅ Nahrajte 2-3 PDF soubory najednou
2. ✅ Zpracujte všechny
3. ✅ Ověřte, že každý má své tlačítko pro stažení
4. ✅ Stáhněte všechny a ověřte obsah

#### Scénář 3: Chybové stavy
1. ✅ Zkuste nahrát neplatný soubor (ne PDF)
2. ✅ Ověřte, že se zobrazí chybová zpráva
3. ✅ Zkuste nahrát poškozený PDF
4. ✅ Ověřte zpracování chyby

#### Scénář 4: UI/UX
1. ✅ Ověřte, že progress bar funguje
2. ✅ Zkontrolujte zobrazení seznamu souborů
3. ✅ Ověřte sidebar s instrukcemi
4. ✅ Zkontrolujte footer

---

## Testování v prohlížeči

### Streamlit Development Mode

Streamlit má vestavěný development režim s užitečnými funkcemi:

1. **Auto-reload**: Aplikace se automaticky obnoví při změně kódu
2. **Debugging**: Použijte `st.write()` pro debugování
3. **Error messages**: Chyby se zobrazují přímo v aplikaci

### Debugging tipy

#### 1. Zobrazení proměnných
```python
# V app.py přidejte:
st.write("Debug info:", variable_name)
st.write("DataFrame shape:", df.shape)
```

#### 2. Zobrazení dat
```python
# Zobrazit DataFrame
st.dataframe(df)

# Zobrazit raw data
st.json(data_dict)
```

#### 3. Kontrola session state
```python
# Zobrazit celý session state
st.write(st.session_state)
```

---

## Testování s různými PDF soubory

### Příprava testovacích dat

1. **Platný PDF soubor**
   - Formát: `Købsrekvisition [číslo] [zkratka].pdf`
   - Obsahuje tabulku s objednávkami

2. **Různé jazyky**
   - Testujte s dánskými i anglickými hlavičkami
   - Ověřte správné mapování sloupců

3. **Různé velikosti**
   - Malý soubor (1-2 stránky)
   - Střední soubor (5-10 stránek)
   - Velký soubor (20+ stránek)

---

## Kontrolní seznam testování

### Funkční testy
- [ ] Aplikace se spustí bez chyb
- [ ] Upload PDF souboru funguje
- [ ] Zpracování jednoho souboru funguje
- [ ] Zpracování více souborů funguje
- [ ] Generování Excel souborů funguje
- [ ] Stažení Excel souborů funguje
- [ ] Progress bar se zobrazuje
- [ ] Chybové zprávy se zobrazují správně

### Datové testy
- [ ] Data jsou správně extrahována z PDF
- [ ] Sloupce mají správné názvy
- [ ] Excel obsahuje všechna data
- [ ] Formát Excelu je správný

### UI/UX testy
- [ ] Všechny texty jsou čitelné
- [ ] Tlačítka fungují
- [ ] Sidebar se zobrazuje
- [ ] Footer se zobrazuje
- [ ] Responsive design funguje

### Edge cases
- [ ] Prázdný PDF soubor
- [ ] Poškozený PDF soubor
- [ ] PDF bez tabulky
- [ ] Velmi velký PDF soubor
- [ ] PDF s neobvyklým formátem

---

## Řešení problémů při testování

### Aplikace se nespustí
```bash
# Zkontrolujte závislosti
pip list | grep streamlit

# Zkontrolujte Python verzi
python --version  # Mělo by být 3.8+

# Zkuste reinstalaci
pip install --upgrade streamlit
```

### Chyby při zpracování PDF
```bash
# Zkontrolujte pdfplumber
pip install --upgrade pdfplumber

# Testujte PDF procesor samostatně
python test_processor.py
```

### Chyby při generování Excelu
```bash
# Zkontrolujte openpyxl
pip install --upgrade openpyxl

# Testujte Excel generování
python -c "import pandas as pd; pd.DataFrame({'test': [1,2,3]}).to_excel('test.xlsx')"
```

---

## Pokročilé testování

### Unit testy (volitelné)

Pro komplexnější testování můžete použít pytest:

```bash
pip install pytest
```

Vytvořte `test_app_unit.py`:

```python
import pytest
from pdf_processor import extract_data_from_pdf
from pathlib import Path

def test_extract_data():
    pdf_path = Path("Købsrekvisition K0145920 EGA.pdf")
    if pdf_path.exists():
        df = extract_data_from_pdf(pdf_path)
        assert not df.empty
        assert 'Cislo' in df.columns
```

Spuštění:
```bash
pytest test_app_unit.py -v
```

---

## Závěr

Po dokončení všech testů byste měli mít jistotu, že:
- ✅ Aplikace funguje správně
- ✅ Všechny funkce jsou otestovány
- ✅ Chybové stavy jsou zpracovány
- ✅ UI/UX je funkční

**Doporučení:** Před nasazením do produkce vždy spusťte všechny testy!

---

**Verze:** 1.0  
**Poslední aktualizace:** 2025-11-07




