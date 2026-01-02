# ⚡ Rychlé nastavení po instalaci Pythonu

## ✅ Krok 1: Restartujte terminál

**DŮLEŽITÉ:** Po instalaci Pythonu musíte **zavřít a znovu otevřít** PowerShell/Command Prompt!

1. Zavřete aktuální okno PowerShell
2. Otevřete nové okno PowerShell
3. Přejděte do adresáře projektu:
   ```powershell
   cd "C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky"
   ```

---

## ✅ Krok 2: Ověřte instalaci Pythonu

V **novém** terminálu zadejte:

```powershell
python --version
```

**Měli byste vidět:** `Python 3.x.x`

**Pokud stále nefunguje, zkuste:**
```powershell
py --version
```

---

## ✅ Krok 3: Nainstalujte závislosti

```powershell
python -m pip install -r requirements.txt
```

**Nebo pokud `python` nefunguje:**
```powershell
py -m pip install -r requirements.txt
```

Počkejte na dokončení instalace (1-2 minuty).

---

## ✅ Krok 4: Spusťte aplikaci

```powershell
python -m streamlit run app.py
```

**Nebo:**
```powershell
py -m streamlit run app.py
```

---

## 🚨 Pokud Python stále není rozpoznán

### Možnost 1: Použijte Python Launcher (py)

Na Windows obvykle funguje `py` místo `python`:

```powershell
py --version
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

### Možnost 2: Zkontrolujte PATH

1. Otevřete "Systémové proměnné prostředí"
   - Stiskněte `Win + R`
   - Zadejte: `sysdm.cpl`
   - Klikněte na "Upřesnit" → "Proměnné prostředí"

2. Zkontrolujte, že Python je v PATH:
   - V "Systémové proměnné" najděte `Path`
   - Měly by tam být cesty jako:
     - `C:\Python3x\`
     - `C:\Python3x\Scripts\`
     - `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\`
     - `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\Scripts\`

3. Pokud Python není v PATH:
   - Přeinstalujte Python
   - **Při instalaci zaškrtněte "Add Python to PATH"**

### Možnost 3: Použijte plnou cestu k Pythonu

Najděte, kde je Python nainstalovaný (obvykle):
- `C:\Python3x\python.exe`
- `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\python.exe`
- `C:\Program Files\Python3x\python.exe`

Pak použijte plnou cestu:
```powershell
"C:\Python3x\python.exe" -m pip install -r requirements.txt
"C:\Python3x\python.exe" -m streamlit run app.py
```

---

## 💡 Nejjednodušší způsob

**Použijte batch soubor:**

1. Dvojklik na `START_APP.bat`
2. Skript automaticky:
   - Najde Python
   - Nainstaluje závislosti
   - Spustí aplikaci

---

## ✅ Očekávaný výsledek

Po úspěšném spuštění uvidíte v terminálu:

```
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

A prohlížeč se automaticky otevře s aplikací!

---

**Potřebujete pomoc?** Zkuste nejprve restartovat terminál a použít `py` místo `python`.




