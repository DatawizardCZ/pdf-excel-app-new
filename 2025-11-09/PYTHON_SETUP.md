# 🐍 Nastavení Python interpretu

## Problém: Python není rozpoznán

Pokud Python není rozpoznán v terminálu, můžete ho nastavit v editoru (VS Code/Cursor).

---

## 📋 Metoda 1: Výběr interpretu v editoru

### V Cursor/VS Code:

1. **Otevřete Command Palette:**
   - Stiskněte: `Ctrl + Shift + P` (nebo `Cmd + Shift + P` na Mac)

2. **Vyberte interpret:**
   - Zadejte: `Python: Select Interpreter`
   - Vyberte z nabídky

3. **Pokud Python není v seznamu:**
   - Klikněte na "Enter interpreter path..."
   - Zadejte cestu k Pythonu (viz níže)

---

## 🔍 Metoda 2: Najít cestu k Pythonu

### Automatické vyhledání:

Spusťte v PowerShell:

```powershell
# Hledání Pythonu v běžných umístěních
$paths = @(
    "C:\Python*",
    "$env:LOCALAPPDATA\Programs\Python\Python*",
    "$env:ProgramFiles\Python*",
    "$env:ProgramFiles(x86)\Python*"
)

foreach ($path in $paths) {
    $found = Get-ChildItem -Path $path -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host "Nalezeno: $($found.FullName)"
        $pythonExe = Join-Path $found.FullName "python.exe"
        if (Test-Path $pythonExe) {
            Write-Host "  Python.exe: $pythonExe" -ForegroundColor Green
        }
    }
}
```

### Manuální hledání:

1. Otevřete Průzkumník souborů
2. Přejděte do:
   - `C:\Python3x\` (kde x je verze)
   - `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\`
   - `C:\Program Files\Python3x\`
3. Hledejte soubor `python.exe`

---

## ✅ Metoda 3: Přidat Python do PATH

### Windows 10/11:

1. **Otevřete Systémové proměnné:**
   - Stiskněte `Win + R`
   - Zadejte: `sysdm.cpl`
   - Klikněte na "Upřesnit" → "Proměnné prostředí"

2. **Upravte PATH:**
   - V "Systémové proměnné" najděte `Path`
   - Klikněte na "Upravit"
   - Klikněte na "Nový"
   - Přidejte cestu k Pythonu (např. `C:\Python311\`)
   - Přidejte také cestu k Scripts (např. `C:\Python311\Scripts\`)
   - Klikněte "OK" na všech oknech

3. **Restartujte terminál**

---

## 🧪 Ověření

Po nastavení zkuste:

```powershell
python --version
```

Nebo použijte plnou cestu:

```powershell
C:\Python311\python.exe --version
```

---

## 💡 Tip: Použijte Python Launcher

Pokud máte Python nainstalovaný, ale není v PATH, můžete použít Python Launcher:

1. Stáhněte Python z: https://www.python.org/downloads/
2. Při instalaci zaškrtněte "Add Python to PATH"
3. Po instalaci restartujte terminál

---

## 🚀 Po nastavení Pythonu

1. **Nainstalujte závislosti:**
   ```powershell
   python -m pip install -r requirements.txt
   ```

2. **Spusťte aplikaci:**
   ```powershell
   python -m streamlit run app.py
   ```

---

## 📝 Poznámka

Pokud Python stále není rozpoznán, zkuste:
- Restartovat počítač
- Přeinstalovat Python s "Add Python to PATH"
- Použít plnou cestu k python.exe v příkazech



