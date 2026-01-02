# 🔍 Jak ověřit, že změny jsou nasazeny na Streamlit Cloud

## ✅ Automatické nasazení

**Ano, Streamlit Cloud automaticky nasazuje změny!**

Když pushnete změny na GitHub:
- ✅ Streamlit Cloud automaticky detekuje změny
- ✅ Spustí nový build (obvykle 1-3 minuty)
- ✅ Nasadí novou verzi aplikace
- ✅ **Není potřeba ruční zásah**

## 📋 Jak ověřit, že vidíte aktualizovanou verzi

### Metoda 1: Zkontrolujte verzi v aplikaci

Po nasazení uvidíte v dolní části aplikace (footer):
```
Darvis - PDF Objednávky | Verze 2.0.0 | PDF Processor v2.0.0 (2025-11-26)
```

**Co to znamená:**
- `Verze 2.0.0` = verze aplikace (`app_secure.py`)
- `PDF Processor v2.0.0 (2025-11-26)` = verze PDF procesoru (`pdf_processor.py`)

**Pokud vidíte nové datum (2025-11-26), máte aktualizovanou verzi!**

### Metoda 2: Zkontrolujte deployment status na Streamlit Cloud

1. Jděte na [share.streamlit.io](https://share.streamlit.io)
2. Přihlaste se a otevřete vaši aplikaci
3. Klikněte na **"Manage app"** (nebo tlačítko s třemi tečkami)
4. Otevřete záložku **"Deployments"**
5. Zkontrolujte **čas posledního deploymentu**
   - Měl by odpovídat času, kdy jste pushnuli změny na GitHub
   - Status by měl být **"Success"** (zelená)

### Metoda 3: Otestujte funkčnost

Nejjednodušší způsob - otestujte, že změny fungují:
1. Nahrajte testovací PDF (např. AAL PDF)
2. Zkontrolujte, že extrakce funguje správně
3. Pokud vidíte očekávané výsledky, máte aktualizovanou verzi

### Metoda 4: Zkontrolujte GitHub commit

1. Jděte na váš GitHub repozitář
2. Zkontrolujte, že váš commit s `pdf_processor.py` je v historii
3. Zkontrolujte čas commitu
4. Porovnejte s časem deploymentu na Streamlit Cloud

## ⚠️ Co dělat, pokud nevidíte aktualizaci

### 1. Zkontrolujte, že jste pushnuli na správný branch

Streamlit Cloud sleduje obvykle branch `main` nebo `master`:
```bash
git branch  # Zkontrolujte aktuální branch
git push origin main  # Pushněte na správný branch
```

### 2. Zkontrolujte build logy

1. Na Streamlit Cloud → "Manage app" → "Logs"
2. Podívejte se na build logy
3. Hledejte chyby nebo varování

### 3. Zkuste manuální redeploy

1. Na Streamlit Cloud → "Manage app"
2. Klikněte na **"Reboot app"** nebo **"Redeploy"**
3. Počkejte na dokončení buildu

### 4. Zkontrolujte, že soubor je v repozitáři

```bash
git ls-files | grep pdf_processor.py
```

Měl by se zobrazit `pdf_processor.py` - pokud ne, přidejte ho:
```bash
git add pdf_processor.py
git commit -m "Update pdf_processor.py"
git push
```

## 📝 Tipy pro rychlejší ověření

### Přidat timestamp do verze

Pokud chcete přesnější ověření, můžete upravit `PDF_PROCESSOR_LAST_UPDATED` v `pdf_processor.py`:

```python
PDF_PROCESSOR_LAST_UPDATED = "2025-11-26 14:30"  # Přidejte čas
```

Pak uvidíte přesný čas aktualizace v aplikaci.

### Sledovat deployment e-maily

Streamlit Cloud může posílat e-maily o úspěšných/neúspěšných deploymentech (pokud máte nastavené v Settings).

## 🎯 Rychlý checklist

- [ ] Pushnul jsem změny na GitHub (`git push`)
- [ ] Čekal jsem 1-3 minuty na deployment
- [ ] Zkontroloval jsem verzi v footeru aplikace
- [ ] Vidím nové datum v "PDF Processor vX.X.X (datum)"
- [ ] Otestoval jsem funkčnost na testovacím PDF

Pokud všechny body jsou ✅, máte aktualizovanou verzi!





