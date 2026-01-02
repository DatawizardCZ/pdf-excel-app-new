# Technické zhodnocení: Power Query vs Python

## Power Query - Výhody
✅ **Žádná instalace** - funguje přímo v Excelu  
✅ **Uživatelsky přívětivé** - vizuální rozhraní, kolegyně může upravovat  
✅ **Integrace s Excelem** - přirozené pro Excel uživatele  
✅ **Automatické obnovení** - stačí kliknout "Refresh"  

## Power Query - Nevýhody
❌ **Omezené možnosti zpracování PDF** - Power Query má slabou podporu pro PDF  
❌ **Složité zpracování víceřádkových položek** - M-language není ideální pro komplexní logiku  
❌ **Problémy s různými jazyky** - těžší detekce a mapování headerů  
❌ **Závislost na verzi Excelu** - potřebuje Office 365 nebo Excel 2016+ s Power Query  

## Python - Výhody
✅ **Výkonné knihovny pro PDF** - PyPDF2, pdfplumber, tabula-py (extrakce tabulek)  
✅ **Flexibilní zpracování** - snadné řešení víceřádkových položek  
✅ **Jazyková nezávislost** - snadná detekce a mapování headerů podle pozice/patternu  
✅ **Snadná údržba a rozšíření** - standardní programování  
✅ **Batch processing** - snadné zpracování více souborů najednou  

## Python - Nevýhody
❌ **Potřeba instalace Pythonu** - u klienta musí být nainstalovaný  
❌ **Závislosti** - potřebné knihovny (pandas, openpyxl, pdfplumber)  
❌ **Méně intuitivní** - pro ne-technické uživatele může být složitější  

---

## Doporučení: **Python s uživatelsky příjemným obalem**

Pro tento projekt doporučuji **Python**, protože:
1. **PDF zpracování** je v Pythonu mnohem robustnější
2. **Víceřádkové položky** se lépe zpracují programově
3. **Jazyková flexibilita** (dánština/angličtina) je snazší řešit

### Možnosti "zaobalení" Pythonu pro uživatele:

#### Varianta 1: **Streamlit Web App** (DOPORUČENO)
- Jednoduché webové rozhraní
- Uživatel nahraje PDF soubory přes prohlížeč
- Klikne na tlačítko "Zpracovat"
- Stáhne si Excel soubory
- **Výhody:**
  - Žádná znalost Pythonu potřeba
  - Funguje na jakémkoli počítači s prohlížečem
  - Moderní, intuitivní UI
  - Snadné nasazení (lokálně nebo na serveru)

#### Varianta 2: **Desktop App s Tkinter/PyQt**
- Klasická desktopová aplikace
- Drag & drop PDF souborů
- Tlačítko "Zpracovat"
- **Výhody:**
  - Funguje offline
  - Nativní aplikace
- **Nevýhody:**
  - Složitější vývoj
  - Potřeba kompilace pro distribuci

#### Varianta 3: **Excel Add-in s Python backendem**
- Excel makro, které volá Python skript
- **Výhody:**
  - Integrace s Excelem
- **Nevýhody:**
  - Složitější setup
  - Závislost na Excelu

#### Varianta 4: **Jednoduchý skript s konfiguračním souborem**
- Python skript + config.json
- Uživatel upraví cestu k PDF v config.json
- Spustí skript (double-click)
- **Výhody:**
  - Nejjednodušší implementace
  - Minimální závislosti
- **Nevýhody:**
  - Méně uživatelsky přívětivé

---

## Doporučené řešení: **Streamlit Web App**

### Proč Streamlit?
1. **Nejjednodušší pro uživatele** - funguje v prohlížeči
2. **Rychlý vývoj** - pár hodin práce
3. **Profesionální vzhled** - moderní UI
4. **Snadné nasazení** - může běžet lokálně nebo na serveru
5. **Bez instalace** - uživatel jen otevře URL

### Jak to bude fungovat:
1. Uživatel spustí aplikaci (lokálně nebo na serveru)
2. Otevře se webové rozhraní v prohlížeči
3. Nahraje PDF soubory (drag & drop nebo výběr)
4. Klikne "Zpracovat objednávky"
5. Stáhne si Excel soubory (jeden soubor = jeden Excel)

### Technický stack:
- **Python 3.8+**
- **Streamlit** - webové rozhraní
- **pdfplumber** nebo **tabula-py** - extrakce z PDF
- **pandas** - zpracování dat
- **openpyxl** - zápis do Excelu

### Implementace u klienta:
**Možnost A - Lokální spuštění:**
- Nainstaluje Python (jednou)
- Nainstaluje závislosti (`pip install -r requirements.txt`)
- Spustí aplikaci (`streamlit run app.py`)
- Otevře se automaticky v prohlížeči

**Možnost B - Server (pokud má klient server):**
- Nasazení na server
- Uživatel přistupuje přes URL
- Žádná instalace na klientských počítačích

**Možnost C - Executable (pokud potřebují bez instalace Pythonu):**
- Zabalit do .exe pomocí PyInstaller
- Dvojklik = spuštění aplikace
- Otevře se v prohlížeči

---

## Shrnutí

**Doporučení: Python + Streamlit**

**Proč:**
- ✅ Lepší zpracování PDF
- ✅ Snadné řešení víceřádkových položek
- ✅ Flexibilní zpracování různých jazyků
- ✅ Uživatelsky příjemné (webové rozhraní)
- ✅ Snadná implementace u klienta
- ✅ Profesionální vzhled

**Alternativa:**
Pokud klient trvá na Power Query, je to možné, ale bude to:
- Složitější implementace
- Méně robustní zpracování PDF
- Těžší údržba

