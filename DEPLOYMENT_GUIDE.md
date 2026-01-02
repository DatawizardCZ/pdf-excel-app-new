# 🚀 Průvodce nasazením na GitHub a deployment

## Krok 1: Příprava projektu pro GitHub

### 1.1 Ověření potřebných souborů

Ujistěte se, že máte všechny potřebné soubory:

**ESSENTIAL FILES (Povinné):**
- ✅ `app_secure.py` - Hlavní aplikace
- ✅ `config.py` - Konfigurační modul
- ✅ `pdf_processor.py` - Zpracování PDF
- ✅ `requirements.txt` - Python závislosti
- ✅ `.gitignore` - Git ignore soubor
- ✅ `.env.example` - Šablona pro environment variables
- ✅ `README.md` - Dokumentace projektu

**OPTIONAL FILES (Volitelné, ale doporučené):**
- `DEPLOYMENT_GUIDE.md` - Tento soubor
- `SECURITY_FEATURES.md` - Dokumentace bezpečnostních funkcí

**FILES TO EXCLUDE (Nepřidávat do Git):**
- ❌ `.env` - Obsahuje citlivá data (hesla)
- ❌ `logs/` - Log soubory
- ❌ `__pycache__/` - Python cache
- ❌ `*.xlsx`, `*.xls` - Vygenerované Excel soubory
- ❌ `*.pdf` - Testovací PDF soubory
- ❌ `pdf_analysis.json` - Dočasné analýzy

### 1.2 Ověření .gitignore

Zkontrolujte, že `.gitignore` obsahuje:
- `.env`
- `logs/`
- `__pycache__/`
- `*.xlsx`, `*.xls`
- `*.pdf` (pokud nechcete commitovat testovací soubory)
- `pdf_analysis.json`

## Krok 2: Inicializace Git repozitáře

### 2.1 Pokud ještě nemáte Git repozitář:

```bash
# Inicializace Git repozitáře
git init

# Přidání všech souborů (respektuje .gitignore)
git add .

# První commit
git commit -m "Initial commit: Darvis PDF Objednávky application"
```

### 2.2 Pokud už máte Git repozitář:

```bash
# Zkontrolujte status
git status

# Přidejte změny
git add .

# Commit změn
git commit -m "Prepare for deployment"
```

## Krok 3: Vytvoření GitHub repozitáře

### 3.1 Na GitHub.com:

1. Přihlaste se na [GitHub.com](https://github.com)
2. Klikněte na **"+"** v pravém horním rohu
3. Vyberte **"New repository"**
4. Vyplňte:
   - **Repository name:** `darvis-pdf-objednavky` (nebo váš název)
   - **Description:** "Bezpečná aplikace pro převod PDF objednávek do Excelu"
   - **Visibility:** Private (doporučeno) nebo Public
   - **NEPŘIDÁVEJTE** README, .gitignore, nebo license (už je máte)
5. Klikněte na **"Create repository"**

### 3.2 Propojení lokálního repozitáře s GitHub:

```bash
# Přidejte remote origin (nahraďte YOUR_USERNAME a REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Nebo pomocí SSH (pokud máte nastavené SSH klíče):
# git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Ověření remote
git remote -v
```

## Krok 4: Push na GitHub

```bash
# Push na GitHub (první push)
git branch -M main
git push -u origin main

# Pro další pushy stačí:
# git push
```

## Krok 5: Nastavení pro deployment

### 5.1 Streamlit Cloud Deployment

1. **Přihlaste se na Streamlit Cloud:**
   - Jděte na [share.streamlit.io](https://share.streamlit.io)
   - Přihlaste se pomocí GitHub účtu
   - **DŮLEŽITÉ:** Při prvním přihlášení autorizujte Streamlit Cloud k přístupu k vašim GitHub repozitářům

2. **Autorizace GitHub přístupu:**
   - Pokud vidíte chybu o "deploy key", postupujte takto:
   - Streamlit Cloud potřebuje přístup k vašemu repozitáři
   - **Možnost A - GitHub App (doporučeno pro organizace):**
     - Pokud jsou deploy keys zakázané v organizaci, použijte GitHub App
     - V Streamlit Cloud Settings → GitHub App klikněte na **"Install GitHub App"**
     - Autorizujte přístup k organizaci a repozitáři
     - GitHub App nevyžaduje deploy keys a funguje i když jsou zakázané
   - **Možnost B - OAuth autorizace:**
     - Při přihlášení na Streamlit Cloud klikněte na **"Authorize Streamlit"** nebo **"Connect GitHub"**
     - Povolte přístup k vašim repozitářům (můžete omezit pouze na konkrétní repozitář)
     - Toto je nejjednodušší způsob pro soukromé i veřejné repozitáře
   - **Možnost C - Deploy Key (pouze pokud jsou povolené):**
     - ⚠️ **NEFUNGUJE** pokud jsou deploy keys zakázané v organizaci!
     - Pokud OAuth nefunguje a deploy keys jsou povolené, můžete nastavit deploy key ručně (viz níže)

3. **Vytvořte novou aplikaci:**
   - Klikněte na **"New app"**
   - Vyberte váš repozitář (měli byste ho vidět, pokud je autorizace úspěšná)
   - Vyberte branch (obvykle `main`)
   - Nastavte **Main file path:** `app_secure.py`

4. **Nastavte Environment Variables:**
   - V Settings → Secrets přidejte:
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

5. **Deploy:**
   - Klikněte na **"Deploy"**
   - Počkejte na dokončení buildu
   - **Typická doba deployment:**
     - **První deployment:** 2-5 minut (instalace závislostí, vytvoření prostředí)
     - **Další deploymenty:** 1-3 minuty (některé části jsou cachované)
     - **Rychlé aktualizace:** 30 sekund - 2 minuty (pouze změny v kódu)
   - Aplikace bude dostupná na `https://your-app-name.streamlit.app`
   - Můžete sledovat progress v Streamlit Cloud dashboardu

#### 5.1.1 Nastavení Deploy Key (pokud OAuth nefunguje)

Pokud Streamlit Cloud stále vyžaduje deploy key, postupujte takto:

1. **Vygenerujte SSH key pár:**
   ```bash
   # Na vašem počítači
   ssh-keygen -t ed25519 -C "streamlit-cloud-deploy" -f ~/.ssh/streamlit_deploy_key
   ```
   - Stiskněte Enter pro výchozí umístění
   - **NEPŘIDÁVEJTE passphrase** (nechte prázdné)

2. **Zkopírujte veřejný klíč:**
   ```bash
   # Windows (PowerShell)
   Get-Content ~/.ssh/streamlit_deploy_key.pub
   
   # Linux/Mac
   cat ~/.ssh/streamlit_deploy_key.pub
   ```

3. **Přidejte Deploy Key na GitHub:**
   - Jděte na váš GitHub repozitář
   - Klikněte na **Settings** → **Deploy keys** → **Add deploy key**
   - **Title:** `Streamlit Cloud Deploy`
   - **Key:** Vložte obsah z `streamlit_deploy_key.pub`
   - ✅ **Zaškrtněte "Allow write access"** (Streamlit Cloud to potřebuje)
   - Klikněte na **"Add key"**

4. **Přidejte Deploy Key do Streamlit Cloud:**
   - V Streamlit Cloud jděte na **Settings** vaší aplikace
   - Najděte sekci **"Deploy key"** nebo **"Repository access"**
   - Vložte **soukromý klíč** (`streamlit_deploy_key` - obsah souboru BEZ .pub)
   - Uložte nastavení

5. **Alternativně - Použijte GitHub App (doporučeno pro organizace):**
   - Streamlit Cloud podporuje GitHub Apps
   - V Settings → GitHub App můžete nainstalovat Streamlit Cloud GitHub App
   - Toto automaticky nastaví potřebná oprávnění
   - **GitHub App nevyžaduje deploy keys** a funguje i když jsou zakázané v organizaci
   - Postup:
     1. V Streamlit Cloud Settings → GitHub App
     2. Klikněte na **"Install GitHub App"** nebo **"Configure"**
     3. Na GitHub vyberte organizaci a repozitář
     4. Klikněte na **"Install"** nebo **"Authorize"**
     5. Vraťte se na Streamlit Cloud a zkuste znovu deploy

**Poznámka:** Pro většinu uživatelů by měla OAuth autorizace (Možnost A) fungovat bez problémů. Deploy key je potřeba pouze v specifických případech.

### 5.2 Alternativní deployment (Docker)

Vytvořte `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Kopírování requirements a instalace závislostí
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování aplikace
COPY app_secure.py config.py pdf_processor.py ./

# Vytvoření adresářů
RUN mkdir -p logs

# Exponování portu
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Spuštění aplikace
CMD ["streamlit", "run", "app_secure.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

A `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - APP_USERNAME=${APP_USERNAME}
      - APP_PASSWORD=${APP_PASSWORD}
      - DEBUG_MODE=false
      - REQUIRE_HTTPS=false
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

## Krok 6: Ověření deployment

### 6.1 Testování lokálně:

```bash
# Spuštění aplikace
streamlit run app_secure.py

# Ověření na http://localhost:8501
```

### 6.2 Testování na Streamlit Cloud:

1. Otevřete URL vaší aplikace
2. Přihlaste se pomocí nastavených credentials
3. Nahrajte testovací PDF soubor
4. Ověřte, že zpracování funguje správně

## Krok 7: Bezpečnostní checklist

Před nasazením do produkce zkontrolujte:

- [ ] ✅ Změněno výchozí heslo v environment variables
- [ ] ✅ `DEBUG_MODE=false` v produkci
- [ ] ✅ `REQUIRE_HTTPS=true` (pokud je HTTPS dostupné)
- [ ] ✅ `.env` soubor není v Git repozitáři
- [ ] ✅ Citlivá data jsou pouze v environment variables
- [ ] ✅ Logy neobsahují citlivé informace
- [ ] ✅ Aplikace běží na HTTPS v produkci
- [ ] ✅ Session timeout je nastaven rozumně
- [ ] ✅ File size limits jsou nastaveny

## Krok 8: Monitoring a údržba

### 8.1 Logy:

- Logy jsou ukládány v `logs/app.log`
- V produkci sledujte logy pro chyby a bezpečnostní incidenty

### 8.2 Aktualizace:

```bash
# Aktualizace závislostí
pip install --upgrade -r requirements.txt

# Commit a push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

## 🔗 Užitečné odkazy

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [GitHub Documentation](https://docs.github.com/)

## ❓ Troubleshooting

### Problém: "Cannot deploy without deploy key" / "Repository access denied"

**Řešení:**
1. **Ověřte GitHub autorizaci:**
   - Jděte na [share.streamlit.io](https://share.streamlit.io)
   - V pravém horním rohu klikněte na váš profil → **Settings**
   - Zkontrolujte sekci **"Connected accounts"** nebo **"GitHub"**
   - Pokud není GitHub připojen, klikněte na **"Connect GitHub"** nebo **"Authorize"**
   - Povolte přístup k vašim repozitářům

2. **Zkontrolujte oprávnění repozitáře:**
   - Ujistěte se, že máte přístup k repozitáři (jste owner nebo collaborator)
   - Pokud je repozitář v organizaci, možná potřebujete povolit Streamlit Cloud v organizačních nastaveních

3. **"Deploy keys are disabled for this organization":**
   - **Řešení 1 (doporučeno):** Použijte GitHub App v Streamlit Cloud Settings
     - Jděte na Settings → GitHub App → Install GitHub App
     - GitHub App nevyžaduje deploy keys a funguje i když jsou zakázané
   - **Řešení 2:** Požádejte organizačního admina o povolení Streamlit Cloud GitHub App
   - **Řešení 3:** Použijte osobní fork repozitáře pro deployment
   - **Řešení 4:** Kontaktujte Streamlit support pro enterprise řešení

4. **Nastavte Deploy Key (pouze pokud jsou povolené):**
   - ⚠️ **NEFUNGUJE** pokud jsou deploy keys zakázané v organizaci!
   - Postupujte podle sekce **5.1.1 Nastavení Deploy Key** výše
   - Nebo použijte GitHub App v Streamlit Cloud Settings

5. **Alternativní řešení:**
   - Dočasně změňte repozitář na Public (Settings → Change visibility)
   - Po úspěšném deployi můžete změnit zpět na Private
   - Streamlit Cloud by měl mít přístup i po změně zpět

### Problém: Aplikace se nespustí na Streamlit Cloud

**Řešení:**
- Zkontrolujte, že všechny závislosti jsou v `requirements.txt`
- Ověřte, že `app_secure.py` je v kořenovém adresáři
- Zkontrolujte logy buildu v Streamlit Cloud
- Ověřte, že Python verze je kompatibilní (Streamlit Cloud podporuje Python 3.7-3.11)

### Problém: Environment variables nefungují

**Řešení:**
- Ověřte, že jsou nastavené v Streamlit Cloud Secrets
- Zkontrolujte syntax (bez mezer kolem `=`)
- Restartujte aplikaci po změně secrets
- Ujistěte se, že v kódu používáte `st.secrets` nebo `os.getenv()` správně

### Problém: Import errors

**Řešení:**
- Ověřte, že všechny moduly jsou v `requirements.txt`
- Zkontrolujte, že cesty k souborům jsou relativní
- Otestujte lokálně před pushnutím
- Zkontrolujte, že všechny importované soubory jsou v repozitáři (ne v `.gitignore`)

### Problém: Deployment trvá příliš dlouho

**Typické časy deployment:**
- ✅ **První deployment:** 2-5 minut (normální)
- ✅ **Další deploymenty:** 1-3 minuty (normální)
- ⚠️ **Více než 10 minut:** Možný problém

**Co ovlivňuje rychlost:**
- Počet závislostí v `requirements.txt` (více = pomaleji)
- Velikost repozitáře (velké soubory = pomaleji)
- Zatížení Streamlit Cloud serverů
- Komplexita buildu (Docker image, atd.)

**Jak zrychlit deployment:**
1. **Optimalizujte `requirements.txt`:**
   - Uveďte pouze potřebné balíčky
   - Zadejte konkrétní verze (např. `streamlit==1.28.0` místo `streamlit>=1.28.0`)
   - Odstraňte nepoužívané závislosti

2. **Snižte velikost repozitáře:**
   - Ujistěte se, že `.gitignore` správně ignoruje velké soubory
   - Necommitujte testovací PDF soubory, logy, cache

3. **Použijte `.streamlit/config.toml`:**
   - Streamlit Cloud může cachovat některé konfigurace

4. **Sledujte build logy:**
   - V Streamlit Cloud klikněte na "Manage app" → "Logs"
   - Zkontrolujte, kde se build zasekává

**Kdy se obávat:**
- ⚠️ Deployment trvá více než 10 minut
- ⚠️ Build se zasekává na instalaci konkrétního balíčku
- ⚠️ Opakované timeouty

**Řešení pro pomalé deploymenty:**
- Zkontrolujte build logy pro chyby
- Zkuste znovu deploy (někdy pomůže)
- Kontaktujte Streamlit support, pokud problém přetrvává

---

**Poznámka:** Tento průvodce předpokládá, že máte základní znalosti Git a GitHub. Pokud potřebujete pomoc, kontaktujte podporu.



