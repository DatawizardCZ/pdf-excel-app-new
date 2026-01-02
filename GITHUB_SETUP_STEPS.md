# 🚀 Rychlý průvodce: Upload na GitHub a příprava pro deployment

## 📋 Krok za krokem

### KROK 1: Ověření souborů ✅

Zkontrolujte, že máte tyto **ESSENTIAL FILES**:

```
✅ app_secure.py          - Hlavní aplikace
✅ config.py              - Konfigurace
✅ pdf_processor.py       - PDF zpracování
✅ requirements.txt      - Závislosti
✅ .gitignore            - Git ignore
✅ .env.example          - Environment template
✅ README.md             - Dokumentace
```

**Ověření:**
```bash
# V PowerShell
Get-ChildItem app_secure.py, config.py, pdf_processor.py, requirements.txt, .gitignore, .env.example, README.md
```

### KROK 2: Ověření .gitignore ✅

Zkontrolujte, že `.gitignore` obsahuje:
- `.env` (důležité - obsahuje hesla!)
- `logs/`
- `__pycache__/`
- `*.xlsx`, `*.xls`
- `*.pdf` (testovací soubory)

### KROK 3: Inicializace Git (pokud ještě není) 🔧

```bash
# Zkontrolujte, zda už máte Git repozitář
git status

# Pokud ne, inicializujte:
git init
```

### KROK 4: Přidání souborů do Git 📦

```bash
# Přidání všech souborů (respektuje .gitignore)
git add .

# Ověření, že .env NENÍ přidán
git status | Select-String ".env"
# Mělo by zobrazit pouze .env.example, NE .env

# Commit
git commit -m "Initial commit: Darvis PDF Objednávky application"
```

### KROK 5: Vytvoření GitHub repozitáře 🌐

1. **Jděte na [GitHub.com](https://github.com)**
2. **Klikněte na "+" → "New repository"**
3. **Vyplňte:**
   - Repository name: `darvis-pdf-objednavky` (nebo váš název)
   - Description: "Bezpečná aplikace pro převod PDF objednávek do Excelu"
   - Visibility: **Private** (doporučeno) nebo Public
   - **NEPŘIDÁVEJTE** README, .gitignore, license (už je máte)
4. **Klikněte "Create repository"**

### KROK 6: Propojení s GitHub 🔗

```bash
# Přidejte remote (nahraďte YOUR_USERNAME a REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Ověření
git remote -v
```

### KROK 7: Push na GitHub ⬆️

```bash
# První push
git branch -M main
git push -u origin main

# Pro další pushy stačí:
# git push
```

### KROK 8: Deployment na Streamlit Cloud ☁️

1. **Jděte na [share.streamlit.io](https://share.streamlit.io)**
2. **Přihlaste se pomocí GitHub účtu**
3. **Klikněte "New app"**
4. **Vyberte:**
   - Repository: váš repozitář
   - Branch: `main`
   - Main file path: `app_secure.py`
5. **V Settings → Secrets přidejte:**
   ```
   APP_USERNAME=your_username
   APP_PASSWORD=your_secure_password
   DEBUG_MODE=false
   REQUIRE_HTTPS=true
   MAX_FILE_SIZE_MB=50
   MAX_FILES_PER_SESSION=20
   SESSION_TIMEOUT=3600
   LOG_LEVEL=INFO
   ```
6. **Klikněte "Deploy"**
7. **Počkejte na dokončení buildu**

---

## ✅ Final Checklist

Před pushnutím zkontrolujte:

- [ ] ✅ Všechny essential files jsou v projektu
- [ ] ✅ `.env` soubor **NENÍ** v Git (zkontrolujte `git status`)
- [ ] ✅ `.env.example` **JE** v Git (šablona bez citlivých dat)
- [ ] ✅ `.gitignore` správně ignoruje citlivé soubory
- [ ] ✅ Aplikace funguje lokálně (`streamlit run app_secure.py`)
- [ ] ✅ Žádné citlivé údaje nejsou v kódu
- [ ] ✅ `requirements.txt` obsahuje všechny závislosti

---

## 📝 Seznam potřebných souborů

### ✅ ESSENTIAL (Povinné):
1. `app_secure.py` - Hlavní aplikace
2. `config.py` - Konfigurace
3. `pdf_processor.py` - PDF zpracování
4. `requirements.txt` - Závislosti
5. `.gitignore` - Git ignore
6. `.env.example` - Environment template
7. `README.md` - Dokumentace

### 📦 OPTIONAL (Doporučené):
- `DEPLOYMENT_GUIDE.md` - Detailní průvodce nasazením
- `FILES_CHECKLIST.md` - Kompletní seznam souborů
- `GITHUB_SETUP_STEPS.md` - Tento soubor

### ❌ EXCLUDE (Nepřidávat):
- `.env` - Obsahuje hesla!
- `logs/` - Log soubory
- `__pycache__/` - Python cache
- `*.xlsx`, `*.xls` - Vygenerované soubory
- `*.pdf` - Testovací PDF soubory

---

## 🔒 Bezpečnostní poznámky

⚠️ **DŮLEŽITÉ:**
- **NIKDY** necommitněte `.env` soubor s reálnými hesly
- Používejte `.env.example` jako šablonu
- V produkci nastavte silná hesla
- Používejte HTTPS v produkci
- Nastavte `DEBUG_MODE=false` v produkci

---

## 🆘 Troubleshooting

**Problém: Git neignoruje .env**
```bash
# Ověřte .gitignore
cat .gitignore | Select-String ".env"

# Pokud .env už byl commitnut, odstraňte ho:
git rm --cached .env
git commit -m "Remove .env from repository"
```

**Problém: Push selhává**
```bash
# Zkontrolujte remote
git remote -v

# Zkontrolujte oprávnění na GitHub
# Možná potřebujete nastavit SSH klíče nebo Personal Access Token
```

**Problém: Aplikace se nespustí na Streamlit Cloud**
- Zkontrolujte, že všechny závislosti jsou v `requirements.txt`
- Ověřte, že `app_secure.py` je v kořenovém adresáři
- Zkontrolujte logy buildu v Streamlit Cloud

---

## 📚 Další dokumentace

- `DEPLOYMENT_GUIDE.md` - Detailní průvodce nasazením
- `FILES_CHECKLIST.md` - Kompletní seznam souborů
- `README.md` - Hlavní dokumentace projektu

---

**Hotovo! 🎉** Váš projekt je připraven pro deployment na GitHub a Streamlit Cloud.














