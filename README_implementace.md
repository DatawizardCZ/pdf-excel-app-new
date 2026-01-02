# Implementační návod - Streamlit aplikace

## Rychlý start

### 1. Instalace závislostí

```bash
pip install -r requirements.txt
```

### 2. Spuštění aplikace

```bash
streamlit run app.py
```

Aplikace se automaticky otevře v prohlížeči na adrese `http://localhost:8501`

## Nasazení u klienta

### Varianta A: Lokální spuštění (doporučeno pro začátek)

1. **Instalace Pythonu** (pokud není nainstalovaný):
   - Stáhnout z https://www.python.org/downloads/
   - Při instalaci zaškrtnout "Add Python to PATH"

2. **Instalace závislostí**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Spuštění aplikace**:
   ```bash
   streamlit run app.py
   ```

4. **Použití**:
   - Aplikace se otevře automaticky v prohlížeči
   - Uživatel nahraje PDF soubory
   - Klikne "Zpracovat objednávky"
   - Stáhne Excel soubory

### Varianta B: Executable soubor (bez instalace Pythonu)

1. **Instalace PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Vytvoření executable**:
   ```bash
   pyinstaller --onefile --name "Darvis_PDF_Objednavky" app.py
   ```

3. **Distribuce**:
   - Vytvoří se soubor `Darvis_PDF_Objednavky.exe` (nebo `.app` na Mac)
   - Uživatel jen dvojklikne a aplikace se spustí

### Varianta C: Server nasazení (pokud má klient server)

1. **Nahrání souborů na server**

2. **Instalace závislostí na serveru**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Spuštění jako služba**:
   ```bash
   streamlit run app.py --server.port 8501
   ```

4. **Přístup**:
   - Uživatelé přistupují přes URL: `http://server-adresa:8501`

## Struktura projektu

```
.
├── app.py                 # Hlavní Streamlit aplikace
├── requirements.txt       # Python závislosti
├── README_implementace.md # Tento soubor
└── pdf_processor.py       # Modul pro zpracování PDF (bude vytvořen)
```

## Další kroky

1. **Analýza PDF struktury** - prozkoumat ukázkové PDF soubory
2. **Implementace extrakce** - vytvořit logiku pro extrakci dat z PDF
3. **Zpracování víceřádkových položek** - implementovat logiku pro druhý řádek
4. **Mapování headerů** - vytvořit mapování dánských/anglických headerů
5. **Testování** - otestovat na všech ukázkových PDF

## Podpora

V případě problémů:
1. Zkontrolovat, že jsou nainstalované všechny závislosti
2. Ověřit, že Python verze je 3.8 nebo vyšší
3. Zkontrolovat logy v konzoli

