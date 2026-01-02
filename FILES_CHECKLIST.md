# 📋 Seznam souborů potřebných pro deployment

## ✅ ESSENTIAL FILES (Povinné soubory)

Tyto soubory **MUSÍ** být v repozitáři pro správné fungování aplikace:

### 1. Hlavní aplikace
- ✅ **`app_secure.py`** - Hlavní Streamlit aplikace (vstupní bod)

### 2. Moduly
- ✅ **`config.py`** - Konfigurační modul (nastavení, environment variables)
- ✅ **`pdf_processor.py`** - Modul pro zpracování PDF souborů

### 3. Závislosti
- ✅ **`requirements.txt`** - Seznam Python balíčků potřebných pro aplikaci

### 4. Konfigurace Git
- ✅ **`.gitignore`** - Soubory a adresáře, které Git ignoruje

### 5. Dokumentace
- ✅ **`README.md`** - Hlavní dokumentace projektu
- ✅ **`DEPLOYMENT_GUIDE.md`** - Průvodce nasazením (doporučeno)
- ✅ **`FILES_CHECKLIST.md`** - Tento soubor

### 6. Environment Variables Template
- ✅ **`.env.example`** - Šablona pro environment variables (bez citlivých dat)

---

## ⚠️ FILES TO EXCLUDE (Nepřidávat do Git)

Tyto soubory/adresáře **NESMÍ** být v repozitáři:

### Citlivá data
- ❌ **`.env`** - Obsahuje skutečné přihlašovací údaje (hesla)
- ❌ **`*.key`**, **`*.pem`**, **`*.crt`** - Bezpečnostní klíče

### Dočasné soubory
- ❌ **`logs/`** - Adresář s log soubory
- ❌ **`__pycache__/`** - Python cache adresář
- ❌ **`*.pyc`**, **`*.pyo`**, **`*.pyd`** - Zkompilované Python soubory

### Vygenerované soubory
- ❌ **`*.xlsx`**, **`*.xls`** - Vygenerované Excel soubory
- ❌ **`pdf_analysis.json`** - Dočasné analýzy

### Testovací soubory
- ❌ **`*.pdf`** - Testovací PDF soubory (pokud nejsou součástí dokumentace)
- ❌ **`test_*.py`** - Testovací skripty (pokud nejsou součástí CI/CD)

### IDE a OS soubory
- ❌ **`.vscode/`**, **`.idea/`** - IDE konfigurace
- ❌ **`.DS_Store`**, **`Thumbs.db`** - OS soubory

---

## 📦 OPTIONAL FILES (Volitelné, ale užitečné)

Tyto soubory mohou být užitečné, ale nejsou povinné:

### Docker (pokud používáte Docker)
- 📦 **`Dockerfile`** - Pro Docker deployment
- 📦 **`docker-compose.yml`** - Pro Docker Compose
- 📦 **`.dockerignore`** - Ignorované soubory pro Docker build

### CI/CD
- 📦 **`.github/workflows/`** - GitHub Actions workflows
- 📦 **`.gitlab-ci.yml`** - GitLab CI konfigurace

### Dokumentace
- 📦 **`SECURITY_FEATURES.md`** - Dokumentace bezpečnostních funkcí
- 📦 **`CHANGELOG.md`** - Historie změn
- 📦 **`LICENSE`** - Licence projektu

---

## 🔍 Ověření před pushnutím

Před pushnutím na GitHub zkontrolujte:

```bash
# 1. Zkontrolujte status
git status

# 2. Ověřte, že .env není v staging area
git status | grep .env
# Mělo by být prázdné nebo zobrazit "nothing to commit"

# 3. Ověřte, že všechny potřebné soubory jsou přidané
ls -la app_secure.py config.py pdf_processor.py requirements.txt .gitignore README.md
# Všechny soubory by měly existovat

# 4. Otestujte aplikaci lokálně
streamlit run app_secure.py
# Aplikace by se měla spustit bez chyb
```

---

## 📝 Struktura finálního repozitáře

Po přípravě by váš repozitář měl vypadat takto:

```
darvis-pdf-objednavky/
├── app_secure.py              ✅ Hlavní aplikace
├── config.py                  ✅ Konfigurace
├── pdf_processor.py           ✅ PDF zpracování
├── requirements.txt           ✅ Závislosti
├── .gitignore                 ✅ Git ignore
├── .env.example               ✅ Environment template
├── README.md                  ✅ Dokumentace
├── DEPLOYMENT_GUIDE.md        ✅ Průvodce nasazením
└── FILES_CHECKLIST.md        ✅ Tento soubor
```

---

## ✅ Final Checklist

Před pushnutím na GitHub:

- [ ] ✅ Všechny essential files jsou v repozitáři
- [ ] ✅ `.env` soubor NENÍ v repozitáři
- [ ] ✅ `.gitignore` správně ignoruje citlivé soubory
- [ ] ✅ `requirements.txt` obsahuje všechny závislosti
- [ ] ✅ `README.md` je aktualizovaný
- [ ] ✅ `.env.example` obsahuje šablonu (bez citlivých dat)
- [ ] ✅ Aplikace funguje lokálně (`streamlit run app_secure.py`)
- [ ] ✅ Žádné citlivé údaje nejsou v kódu
- [ ] ✅ Logy a dočasné soubory jsou ignorovány

---

**Poznámka:** Pokud máte pochybnosti o tom, zda soubor přidat nebo ne, raději ho NEpřidávejte. Můžete ho vždy přidat později, ale odstranění citlivých dat z Git historie je obtížné.














