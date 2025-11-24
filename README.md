# Darvis - PDF Objednávky

Bezpečná Streamlit aplikace pro převod PDF objednávek do Excelu.

## 🚀 Funkce

- ✅ Autentizace uživatelů
- ✅ Validace nahrávaných souborů
- ✅ Omezení velikosti a počtu souborů
- ✅ Bezpečné zpracování chyb
- ✅ Logging aktivit
- ✅ Session management
- ✅ Převod PDF objednávek do Excel formátu

## 📋 Požadavky

- Python 3.8 nebo vyšší
- Streamlit 1.28.0 nebo vyšší

## 🔧 Instalace

1. Naklonujte repozitář:
```bash
git clone <repository-url>
cd 2025-11_Darvis_PDF_objednavky
```

2. Vytvořte virtuální prostředí:
```bash
python -m venv venv
```

3. Aktivujte virtuální prostředí:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

5. Vytvořte soubor `.env` z `.env.example`:
```bash
cp .env.example .env
```

6. Upravte `.env` soubor s vašimi přihlašovacími údaji:
```
APP_USERNAME=your_username
APP_PASSWORD=your_secure_password
```

## ▶️ Spuštění

```bash
streamlit run app_secure.py
```

Aplikace bude dostupná na `http://localhost:8501`

## 🔒 Bezpečnost

⚠️ **DŮLEŽITÉ PRO PRODUKCI:**

1. Změňte výchozí přihlašovací údaje v `.env` souboru
2. Nastavte `DEBUG_MODE=false` v produkci
3. Použijte HTTPS v produkčním prostředí
4. Nastavte `REQUIRE_HTTPS=true` pro vynucení HTTPS
5. Pravidelně kontrolujte logy v `logs/app.log`

## 📁 Struktura projektu

```
.
├── app_secure.py          # Hlavní aplikace
├── config.py              # Konfigurační modul
├── pdf_processor.py       # Zpracování PDF
├── requirements.txt       # Python závislosti
├── .env.example           # Šablona pro environment variables
├── .gitignore            # Git ignore soubor
└── README.md             # Tento soubor
```

## 🌐 Nasazení

### Streamlit Cloud

1. Pushněte kód na GitHub
2. Přihlaste se na [Streamlit Cloud](https://streamlit.io/cloud)
3. Klikněte na "New app"
4. Vyberte repozitář a branch
5. Nastavte environment variables v Settings:
   - `APP_USERNAME`
   - `APP_PASSWORD`
   - `DEBUG_MODE=false`
   - `REQUIRE_HTTPS=true`

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_secure.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📝 Konfigurace

Všechny konfigurační možnosti jsou v `config.py` a lze je přepsat pomocí environment variables:

- `APP_USERNAME` - Uživatelské jméno pro přihlášení
- `APP_PASSWORD` - Heslo pro přihlášení
- `MAX_FILE_SIZE_MB` - Maximální velikost souboru (výchozí: 50 MB)
- `MAX_FILES_PER_SESSION` - Maximální počet souborů (výchozí: 20)
- `SESSION_TIMEOUT` - Timeout relace v sekundách (výchozí: 3600)
- `DEBUG_MODE` - Debug mód (true/false)
- `LOG_LEVEL` - Úroveň logování (DEBUG, INFO, WARNING, ERROR)

## 📄 Licence

Všechna práva vyhrazena.

## 👤 Autor

Darvis - PDF Objednávky

## 🆘 Podpora

Pro problémy nebo dotazy vytvořte issue v repozitáři.


