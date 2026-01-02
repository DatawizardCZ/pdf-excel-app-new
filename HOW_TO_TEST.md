# 🧪 Jak testovat app.py

## Rychlý start

### 1. Spuštění aplikace (nejjednodušší test)

```bash
streamlit run app.py
```

Aplikace se otevře na: **http://localhost:8501**

**Co testovat:**
- ✅ Otevře se aplikace v prohlížeči
- ✅ Nahrajte PDF soubor (např. `Købsrekvisition K0145920 EGA.pdf`)
- ✅ Klikněte na "Zpracovat objednávky"
- ✅ Stáhněte vygenerovaný Excel soubor
- ✅ Ověřte, že Excel obsahuje správná data

---

### 2. Automatické testy (pokud máte Python)

```bash
# Windows
py test_app.py

# Nebo
python test_app.py

# Linux/Mac
python3 test_app.py
```

**Co testy dělají:**
- ✅ Testují zpracování PDF souborů
- ✅ Testují generování Excel souborů
- ✅ Simulují upload souborů
- ✅ Testují zpracování více souborů

---

## Detailní testovací scénáře

### Test 1: Základní funkčnost

1. **Spusťte aplikaci:**
   ```bash
   streamlit run app.py
   ```

2. **V prohlížeči:**
   - Otevřete `http://localhost:8501`
   - Měli byste vidět hlavní stránku s tlačítkem pro upload

3. **Nahrajte PDF:**
   - Klikněte na "Vyberte PDF soubory s objednávkami"
   - Vyberte jeden PDF soubor (např. `Købsrekvisition K0145920 EGA.pdf`)
   - Měli byste vidět: "✅ Načteno 1 souborů"

4. **Zpracujte:**
   - Klikněte na "🔄 Zpracovat objednávky"
   - Měli byste vidět progress bar
   - Po dokončení: "✅ Úspěšně zpracováno 1 souborů"

5. **Stáhněte Excel:**
   - Klikněte na tlačítko "⬇️ [název]_processed.xlsx"
   - Otevřete stažený Excel soubor
   - Ověřte, že obsahuje data z PDF

---

### Test 2: Více souborů

1. **Nahrajte více PDF:**
   - Vyberte 2-3 PDF soubory najednou (držte Ctrl při výběru)
   - Měli byste vidět: "✅ Načteno X souborů"

2. **Zpracujte všechny:**
   - Klikněte na "Zpracovat objednávky"
   - Progress bar by měl ukazovat postup

3. **Stáhněte všechny:**
   - Měli byste vidět tlačítka pro každý soubor
   - Stáhněte všechny a ověřte obsah

---

### Test 3: Chybové stavy

1. **Neplatný soubor:**
   - Zkuste nahrát soubor, který není PDF (např. .txt, .docx)
   - Streamlit by měl automaticky filtrovat pouze PDF

2. **Poškozený PDF:**
   - Pokud máte poškozený PDF, zkuste ho nahrát
   - Měla by se zobrazit chybová zpráva

---

### Test 4: UI/UX

Zkontrolujte:
- ✅ Sidebar s instrukcemi se zobrazuje
- ✅ Progress bar funguje při zpracování
- ✅ Seznam nahraných souborů se zobrazuje
- ✅ Footer se zobrazuje
- ✅ Všechny texty jsou čitelné

---

## Testování pomocí test_app.py

Pokud máte Python nainstalovaný, můžete spustit automatické testy:

### Co potřebujete:
- Python 3.8+
- Nainstalované závislosti: `pip install -r requirements.txt`
- Alespoň jeden PDF soubor v adresáři (formát: `Købsrekvisition*.pdf`)

### Spuštění:

```bash
# Windows
py test_app.py

# Linux/Mac
python3 test_app.py
```

### Výstup testů:

Testy vypíší:
- ✅ Které PDF soubory byly testovány
- ✅ Kolik řádků bylo extrahováno
- ✅ Jaké sloupce obsahuje výsledný DataFrame
- ✅ Zda Excel soubory byly úspěšně vygenerovány
- ✅ Shrnutí: kolik testů prošlo/selhalo

---

## Testování pomocí test_processor.py

Jednodušší test, který testuje pouze PDF procesor:

```bash
py test_processor.py
```

Tento test:
- ✅ Načte konkrétní PDF soubor
- ✅ Extrahuje data
- ✅ Vytvoří Excel soubor
- ✅ Zobrazí výsledky

---

## Řešení problémů

### Aplikace se nespustí

**Chyba:** `streamlit: command not found`

**Řešení:**
```bash
# Nainstalujte Streamlit
pip install streamlit

# Nebo nainstalujte všechny závislosti
pip install -r requirements.txt
```

### Python není nalezen

**Chyba:** `Python was not found`

**Řešení:**
1. Nainstalujte Python z https://www.python.org/downloads/
2. Při instalaci zaškrtněte "Add Python to PATH"
3. Restartujte terminál

### Chyby při zpracování PDF

**Možné příčiny:**
- PDF soubor je poškozený
- PDF nemá očekávaný formát
- Chybí závislosti (pdfplumber)

**Řešení:**
```bash
# Zkontrolujte závislosti
pip install --upgrade pdfplumber pandas openpyxl

# Testujte PDF procesor samostatně
py test_processor.py
```

---

## Rychlý kontrolní seznam

Před nasazením ověřte:

- [ ] Aplikace se spustí bez chyb
- [ ] Upload PDF funguje
- [ ] Zpracování funguje
- [ ] Excel se generuje správně
- [ ] Stažení funguje
- [ ] Více souborů funguje
- [ ] Chybové zprávy se zobrazují
- [ ] UI vypadá dobře

---

## Tipy pro efektivní testování

1. **Použijte různé PDF soubory:**
   - Různé velikosti
   - Různé jazyky (dánština/angličtina)
   - Různé formáty

2. **Testujte edge cases:**
   - Prázdný PDF (pokud existuje)
   - Velmi velký PDF
   - PDF s neobvyklým formátem

3. **Kontrolujte data:**
   - Otevřete vygenerovaný Excel
   - Ověřte, že všechna data jsou správně
   - Zkontrolujte názvy sloupců

4. **Testujte UI:**
   - Zkuste různé velikosti okna prohlížeče
   - Ověřte, že vše je čitelné
   - Zkontrolujte všechny tlačítka

---

## Závěr

**Nejjednodušší způsob testování:**
1. Spusťte: `streamlit run app.py`
2. Otevřete v prohlížeči
3. Nahrajte PDF a otestujte

**Pro automatické testy:**
1. Spusťte: `py test_app.py`
2. Zkontrolujte výstup

**Pro detailní testování:**
- Přečtěte si `TESTING_GUIDE.md`

---

**Potřebujete pomoc?** Zkontrolujte logy nebo spusťte testy s `-v` (verbose) pro více informací.




