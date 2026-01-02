# ⏱️ Streamlit Cloud - Časy deployment

## ✅ Normální časy deployment

### První deployment (nová aplikace)
- **Čas:** 2-5 minut
- **Proč tak dlouho:**
  - Vytvoření nového prostředí
  - Instalace všech závislostí z `requirements.txt`
  - Stahování Python balíčků
  - Build Docker image
  - Nastavení aplikace

### Další deploymenty (aktualizace)
- **Čas:** 1-3 minuty
- **Proč rychleji:**
  - Některé části jsou cachované
  - Docker image může být částečně znovu použit
  - Instalují se pouze změněné závislosti

### Rychlé aktualizace (pouze změny v kódu)
- **Čas:** 30 sekund - 2 minuty
- **Kdy:**
  - Změny pouze v Python souborech
  - Žádné změny v `requirements.txt`
  - Žádné změny v konfiguraci

---

## 📊 Co ovlivňuje rychlost

### 1. Počet závislostí
- **Málo balíčků (5-10):** ~2-3 minuty
- **Středně balíčků (10-20):** ~3-5 minut
- **Hodně balíčků (20+):** ~5-10 minut

**Váš projekt:** 6 balíčků → **očekávaný čas: 2-3 minuty** ✅

### 2. Velikost balíčků
- Některé balíčky jsou velké (např. `pandas`, `numpy`)
- `tabula-py` může být pomalejší (má Java závislosti)
- Váš `requirements.txt` je rozumný

### 3. Zatížení serverů
- Streamlit Cloud sdílí zdroje mezi všemi uživateli
- V špičce může být pomalejší
- Obvykle není problém

### 4. Velikost repozitáře
- Velké soubory v repozitáři zpomalují stahování
- Ujistěte se, že `.gitignore` ignoruje velké soubory

---

## ⚡ Jak zrychlit deployment

### 1. Optimalizujte `requirements.txt`

**Před (pomalejší):**
```txt
streamlit>=1.28.0
pandas>=2.0.0
pdfplumber>=0.10.0
openpyxl>=3.1.0
tabula-py>=2.5.0
python-dotenv>=1.0.0
```

**Po (rychlejší - pokud to funguje):**
```txt
streamlit==1.28.0
pandas==2.0.0
pdfplumber==0.10.0
openpyxl==3.1.0
tabula-py==2.5.0
python-dotenv==1.0.0
```

**Proč:** Konkrétní verze jsou rychlejší na instalaci než rozsahy verzí.

### 2. Odstraňte nepoužívané závislosti
- Zkontrolujte, které balíčky skutečně používáte
- Odstraňte ty, které nejsou potřeba

### 3. Snižte velikost repozitáře
- Ujistěte se, že `.gitignore` obsahuje:
  ```
  *.pdf
  *.xlsx
  *.xls
  logs/
  __pycache__/
  .env
  ```

### 4. Použijte `.streamlit/config.toml`
- Některé konfigurace mohou být cachované
- Vytvořte `.streamlit/config.toml` s vašimi nastaveními

---

## 🚨 Kdy se obávat

### ⚠️ Deployment trvá více než 10 minut
- **Možné příčiny:**
  - Problém s instalací konkrétního balíčku
  - Chyba v buildu
  - Problém na straně Streamlit Cloud

- **Co dělat:**
  1. Zkontrolujte build logy v Streamlit Cloud
  2. Zkuste znovu deploy
  3. Pokud problém přetrvává, kontaktujte support

### ⚠️ Build se zasekává
- **Možné příčiny:**
  - Konflikt verzí závislostí
  - Problém s `tabula-py` (vyžaduje Java)
  - Network timeout

- **Co dělat:**
  1. Zkontrolujte logy, kde se zasekává
  2. Zkuste aktualizovat verze v `requirements.txt`
  3. Pokud je problém s `tabula-py`, zvažte alternativu

### ⚠️ Opakované timeouty
- **Možné příčiny:**
  - Příliš mnoho závislostí
  - Velký repozitář
  - Problém na straně Streamlit Cloud

- **Co dělat:**
  1. Snižte počet závislostí
  2. Zkontrolujte velikost repozitáře
  3. Kontaktujte Streamlit support

---

## 📈 Sledování deployment

### V Streamlit Cloud:
1. Otevřete vaši aplikaci
2. Klikněte na **"Manage app"** (⚙️)
3. Klikněte na **"Logs"**
4. Sledujte build progress

### Co hledat v logech:
- ✅ `Successfully installed...` - dobré znamení
- ⚠️ `ERROR` nebo `FAILED` - problém
- ⚠️ `Timeout` - příliš dlouhý build
- ⚠️ `ModuleNotFoundError` - chybějící závislost

---

## 💡 Tipy

1. **První deployment je vždy nejpomalejší** - to je normální
2. **Další deploymenty jsou rychlejší** - díky cache
3. **Deployment během špičky může být pomalejší** - zkuste později
4. **Sledujte logy** - pomůže identifikovat problémy
5. **Buďte trpěliví** - 2-5 minut je normální pro první deployment

---

## ✅ Váš projekt

**Aktuální `requirements.txt`:**
- 6 balíčků (rozumné množství)
- Žádné problematické závislosti
- **Očekávaný čas: 2-3 minuty** ✅

**Pokud deployment trvá 2-5 minut, je to normální!**

---

## 🔗 Užitečné odkazy

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Support](https://support.streamlit.io/)












