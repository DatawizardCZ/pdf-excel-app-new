# 🚀 Jak spustit START_APP_FIXED.bat

## Metoda 1: Dvojklik (Nejjednodušší) ✅

1. **Otevřete Průzkumník Windows** (File Explorer)
2. **Přejděte do složky projektu:**
   ```
   C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky
   ```
3. **Najděte soubor:** `START_APP_FIXED.bat`
4. **Dvojklikněte** na něj
5. Otevře se černé okno (Command Prompt)
6. Aplikace se spustí automaticky

---

## Metoda 2: Z terminálu

### V PowerShell nebo Command Prompt:

```powershell
cd "C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky"
.\START_APP_FIXED.bat
```

### Nebo přímo:

```powershell
& "C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky\START_APP_FIXED.bat"
```

---

## Metoda 3: Z Cursoru

1. **Otevřete terminál v Cursoru:**
   - Stiskněte `` Ctrl + ` `` (backtick)
   - Nebo: View → Terminal

2. **Spusťte:**
   ```powershell
   .\START_APP_FIXED.bat
   ```

---

## Co se stane po spuštění?

1. ✅ Otevře se černé okno (Command Prompt)
2. ✅ Zkontroluje se, že všechny soubory existují
3. ✅ Spustí se Streamlit aplikace
4. ✅ Zobrazí se zpráva: "Local URL: http://localhost:8501"
5. ✅ Automaticky se otevře prohlížeč s aplikací

---

## Důležité poznámky

⚠️ **Nezavírejte černé okno!**
- Pokud zavřete okno, aplikace se ukončí
- Okno musí zůstat otevřené, dokud používáte aplikaci

⚠️ **Pro zastavení:**
- Stiskněte `Ctrl + C` v černém okně
- Nebo zavřete okno

---

## Pokud se nic nestane

1. **Zkontrolujte, že jste ve správné složce**
2. **Zkontrolujte, že soubor existuje:**
   ```powershell
   dir START_APP_FIXED.bat
   ```
3. **Zkuste spustit jako správce:**
   - Klikněte pravým tlačítkem na soubor
   - Vyberte "Spustit jako správce"

---

## Nejjednodušší způsob

**Dvojklik na soubor v Průzkumníku Windows!** 🖱️

To je vše - aplikace se spustí automaticky.


