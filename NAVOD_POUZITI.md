# Návod k použití aplikace

## 🚀 Spuštění aplikace

### První spuštění (instalace závislostí):
```bash
cd "/Users/karelsimek/Library/CloudStorage/OneDrive-Sdílenéknihovny–Datawizard/Hub - Dokumenty/01_Projekty/2025-11 Darvis-PDF-Objednávky"
pip3 install -r requirements.txt
```

### Spuštění aplikace:
```bash
python3 -m streamlit run app.py
```

Aplikace se automaticky otevře v prohlížeči na adrese: **http://localhost:8501**

---

## 📖 Jak aplikaci použít

### Krok 1: Otevřete aplikaci
- Po spuštění příkazu výše se automaticky otevře prohlížeč
- Nebo ručně otevřete: **http://localhost:8501**

### Krok 2: Nahrajte PDF soubory
- V aplikaci klikněte na tlačítko **"Vyberte PDF soubory s objednávkami"**
- Vyberte jeden nebo více PDF souborů (např. `Købsrekvisition K0145913 TIL.pdf`)
- Můžete vybrat více souborů najednou (držte Ctrl/Cmd při výběru)

### Krok 3: Zpracujte objednávky
- Po nahrání souborů uvidíte jejich seznam
- Klikněte na velké tlačítko **"🔄 Zpracovat objednávky"**
- Aplikace zpracuje všechny nahrané PDF soubory

### Krok 4: Stáhněte Excel soubory
- Po zpracování se zobrazí tlačítka pro stažení
- Každý PDF soubor má své vlastní tlačítko pro stažení Excelu
- Klikněte na tlačítko **"⬇️ [název souboru]_processed.xlsx"** pro stažení

---

## ⚠️ Důležité poznámky

1. **Aplikace je zatím v kostře** - logika pro extrakci dat z PDF ještě není implementovaná
2. **Pro plné fungování** je potřeba dokončit implementaci extrakce dat z PDF
3. **Aplikace běží na pozadí** - po zavření terminálu se ukončí

---

## 🛑 Zastavení aplikace

- V terminálu stiskněte **Ctrl+C**
- Nebo zavřete okno terminálu

---

## 🔧 Řešení problémů

### Aplikace se nespustí
- Zkontrolujte, že máte nainstalovaný Python 3.8+
- Ověřte instalaci závislostí: `pip3 list | grep streamlit`

### Stránka se nenačte
- Zkuste obnovit stránku (F5 nebo Cmd+R)
- Zkontrolujte, že aplikace běží v terminálu
- Zkuste jiný prohlížeč

### Chyba při zpracování
- Zkontrolujte formát PDF souborů
- Ověřte, že PDF soubory nejsou poškozené
- Podívejte se na detaily chyby v aplikaci

