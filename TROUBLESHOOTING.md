# 🔧 Řešení problémů - "Localhost odmítl připojení"

## Problém: Web localhost odmítl připojení

Tento problém znamená, že Streamlit aplikace neběží nebo běží na jiném portu.

---

## ✅ Řešení krok za krokem

### Krok 1: Ověřte, že máte nainstalovaný Python

```bash
py --version
```

Pokud se zobrazí verze (např. `Python 3.11.x`), máte Python nainstalovaný.

**Pokud ne:**
1. Stáhněte Python z: https://www.python.org/downloads/
2. Při instalaci **zaškrtněte "Add Python to PATH"**
3. Restartujte terminál

---

### Krok 2: Nainstalujte závislosti

```bash
py -m pip install -r requirements.txt
```

Nebo jednotlivě:
```bash
py -m pip install streamlit pandas pdfplumber openpyxl
```

---

### Krok 3: Spusťte aplikaci

**Z aktuálního adresáře:**

```bash
py -m streamlit run app.py
```

**Měli byste vidět výstup podobný tomuto:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

### Krok 4: Otevřete v prohlížeči

1. **Automaticky:** Streamlit by měl automaticky otevřít prohlížeč
2. **Manuálně:** Zkopírujte URL z terminálu (obvykle `http://localhost:8501`)

---

## 🚨 Časté problémy a řešení

### Problém 1: "streamlit: command not found"

**Řešení:**
```bash
# Použijte py -m streamlit místo streamlit
py -m streamlit run app.py
```

---

### Problém 2: "Port 8501 je již obsazený"

**Řešení A: Použijte jiný port**
```bash
py -m streamlit run app.py --server.port 8502
```

Pak otevřete: `http://localhost:8502`

**Řešení B: Najděte a ukončete proces na portu 8501**

Windows:
```powershell
# Najít proces
netstat -ano | findstr :8501

# Ukončit proces (nahraďte PID číslem z předchozího příkazu)
taskkill /PID [číslo] /F
```

---

### Problém 3: "ModuleNotFoundError: No module named 'streamlit'"

**Řešení:**
```bash
py -m pip install streamlit
```

---

### Problém 4: Aplikace se spustí, ale prohlížeč se neotevře

**Řešení:**
1. Zkopírujte URL z terminálu (např. `http://localhost:8501`)
2. Vložte do prohlížeče manuálně

---

### Problém 5: "Permission denied" nebo chyby s oprávněními

**Řešení:**
- Spusťte PowerShell jako správce
- Nebo použijte jiný port: `--server.port 8502`

---

## 📋 Kontrolní seznam

Před spuštěním ověřte:

- [ ] Python je nainstalovaný (`py --version`)
- [ ] Streamlit je nainstalovaný (`py -m pip list | findstr streamlit`)
- [ ] Jste v správném adresáři (kde je `app.py`)
- [ ] Port 8501 není obsazený jiným procesem
- [ ] Firewall neblokuje připojení

---

## 🧪 Test, zda vše funguje

### 1. Test Streamlit instalace

```bash
py -m streamlit --version
```

Měli byste vidět verzi Streamlit.

### 2. Test spuštění aplikace

```bash
py -m streamlit run app.py
```

**Očekávaný výstup:**
```
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### 3. Otevření v prohlížeči

- Klikněte na URL v terminálu
- Nebo zkopírujte a vložte do prohlížeče
- Nebo otevřete: `http://localhost:8501`

---

## 🔍 Debugging

### Zobrazit více informací

```bash
py -m streamlit run app.py --logger.level=debug
```

### Zkontrolovat, co běží na portu

```bash
netstat -ano | findstr :8501
```

### Zkontrolovat logy

Streamlit logy se zobrazují přímo v terminálu. Hledejte chybové zprávy.

---

## 💡 Alternativní způsoby spuštění

### Varianta 1: S explicitním portem

```bash
py -m streamlit run app.py --server.port 8501
```

### Varianta 2: S explicitní adresou

```bash
py -m streamlit run app.py --server.address localhost --server.port 8501
```

### Varianta 3: Bez automatického otevření prohlížeče

```bash
py -m streamlit run app.py --server.headless true
```

---

## 🆘 Pokud nic nepomůže

1. **Zkontrolujte, že jste v správném adresáři:**
   ```bash
   dir app.py
   ```
   Měli byste vidět `app.py` v seznamu.

2. **Zkuste reinstalaci Streamlit:**
   ```bash
   py -m pip uninstall streamlit
   py -m pip install streamlit
   ```

3. **Zkuste jiný port:**
   ```bash
   py -m streamlit run app.py --server.port 8502
   ```
   Pak otevřete: `http://localhost:8502`

4. **Zkontrolujte firewall:**
   - Windows Firewall může blokovat připojení
   - Zkuste dočasně vypnout firewall pro test

---

## ✅ Úspěšné spuštění

Pokud vše funguje, měli byste vidět:
- ✅ Streamlit aplikaci v prohlížeči
- ✅ Hlavní stránku s tlačítkem pro upload PDF
- ✅ Sidebar s instrukcemi

---

**Potřebujete další pomoc?** Zkontrolujte chybové zprávy v terminálu a sdílejte je pro další diagnostiku.




