# 🚀 Jak spustit aplikaci - Krok za krokem

## ⚠️ Problém: "Localhost odmítl připojení"

Tento problém znamená, že **aplikace neběží**. Musíte ji nejprve spustit!

---

## 📋 Krok 1: Ověřte, zda máte Python

Otevřete PowerShell nebo Command Prompt a zadejte:

```bash
python --version
```

### ✅ Pokud se zobrazí verze (např. `Python 3.11.5`)
→ Máte Python! Přejděte na **Krok 2**.

### ❌ Pokud se zobrazí "Python was not found"
→ **Musíte nainstalovat Python!** Postupujte podle níže.

---

## 📥 Krok 1a: Instalace Pythonu (pokud nemáte)

1. **Stáhněte Python:**
   - Jděte na: https://www.python.org/downloads/
   - Klikněte na velké žluté tlačítko "Download Python"
   - Stáhne se instalační soubor (např. `python-3.11.5-amd64.exe`)

2. **Nainstalujte Python:**
   - Spusťte stažený soubor
   - **DŮLEŽITÉ:** Na první obrazovce **ZAŠKRTNĚTE** ✅ "Add Python to PATH"
   - Klikněte "Install Now"
   - Počkejte na dokončení instalace

3. **Ověřte instalaci:**
   - **Zavřete a znovu otevřete** PowerShell/Command Prompt
   - Zadejte: `python --version`
   - Měli byste vidět verzi Pythonu

---

## 📦 Krok 2: Instalace závislostí

Otevřete PowerShell/Command Prompt v adresáři s projektem a zadejte:

```bash
python -m pip install -r requirements.txt
```

**Nebo jednotlivě:**
```bash
python -m pip install streamlit pandas pdfplumber openpyxl
```

**Počkejte na dokončení instalace** (může trvat 1-2 minuty).

---

## 🚀 Krok 3: Spuštění aplikace

V **stejném terminálu** zadejte:

```bash
python -m streamlit run app.py
```

**Měli byste vidět něco jako:**
```
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## 🌐 Krok 4: Otevření v prohlížeči

### Automaticky:
- Streamlit by měl **automaticky otevřít** prohlížeč
- Pokud se neotevře, zkopírujte URL z terminálu

### Manuálně:
1. Zkopírujte URL z terminálu: `http://localhost:8501`
2. Vložte do prohlížeče (Chrome, Edge, Firefox)
3. Stiskněte Enter

---

## ✅ Úspěch!

Pokud vše funguje, měli byste vidět:
- ✅ Streamlit aplikaci v prohlížeči
- ✅ Hlavní stránku s nápisem "📄 Převod PDF objednávek do Excelu"
- ✅ Tlačítko pro upload PDF souborů
- ✅ Sidebar s instrukcemi

---

## 🚨 Časté problémy

### Problém: "python: command not found"

**Řešení:**
1. Zkontrolujte, že jste Python nainstalovali
2. **Zavřete a znovu otevřete** terminál
3. Zkuste: `python --version`

### Problém: "ModuleNotFoundError: No module named 'streamlit'"

**Řešení:**
```bash
python -m pip install streamlit
```

### Problém: "Port 8501 is already in use"

**Řešení:**
- Použijte jiný port:
```bash
python -m streamlit run app.py --server.port 8502
```
- Pak otevřete: `http://localhost:8502`

### Problém: Aplikace se spustí, ale prohlížeč se neotevře

**Řešení:**
1. Zkopírujte URL z terminálu (např. `http://localhost:8501`)
2. Vložte do prohlížeče manuálně

---

## 📝 Důležité poznámky

1. **Terminál musí zůstat otevřený!**
   - Pokud zavřete terminál, aplikace se ukončí
   - Pro trvalé spuštění použijte službu nebo Docker

2. **První spuštění může trvat déle**
   - Streamlit stahuje některé komponenty při prvním spuštění

3. **Pokud změníte kód**
   - Streamlit automaticky detekuje změny
   - Klikněte na "Rerun" v aplikaci nebo obnovte stránku

---

## 🛑 Zastavení aplikace

V terminálu stiskněte: **Ctrl + C**

---

## 💡 Tipy

- **Udržujte terminál otevřený** - aplikace běží, dokud terminál neuzavřete
- **Zkontrolujte výstup v terminálu** - zobrazují se tam chyby a logy
- **Použijte správný adresář** - ujistěte se, že jste v adresáři s `app.py`

---

## 🆘 Stále to nefunguje?

1. **Zkontrolujte, že jste v správném adresáři:**
   ```bash
   dir app.py
   ```
   Měli byste vidět `app.py` v seznamu.

2. **Zkuste reinstalaci Streamlit:**
   ```bash
   python -m pip uninstall streamlit
   python -m pip install streamlit
   ```

3. **Zkontrolujte firewall:**
   - Windows Firewall může blokovat připojení
   - Zkuste dočasně vypnout firewall pro test

4. **Zkuste jiný port:**
   ```bash
   python -m streamlit run app.py --server.port 8502
   ```

---

**Potřebujete další pomoc?** Zkontrolujte soubor `TROUBLESHOOTING.md` pro více detailů.




