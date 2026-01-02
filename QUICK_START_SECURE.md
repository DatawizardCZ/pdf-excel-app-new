# 🚀 Rychlý start - Bezpečná verze aplikace

## Krok 1: Instalace závislostí

```bash
pip install -r requirements.txt
```

## Krok 2: Konfigurace bezpečnosti

### Varianta A: Použití .env souboru (Doporučeno)

1. Zkopírujte příklad konfigurace:
```bash
cp .env.example .env
```

2. Upravte soubor `.env` a nastavte:
   - `APP_USERNAME` - vaše uživatelské jméno
   - `APP_PASSWORD` - silné heslo (min. 12 znaků)

### Varianta B: Environment variables

#### Windows (PowerShell):
```powershell
$env:APP_USERNAME="vas_username"
$env:APP_PASSWORD="vase_silne_heslo"
```

#### Linux/Mac:
```bash
export APP_USERNAME="vas_username"
export APP_PASSWORD="vase_silne_heslo"
```

## Krok 3: Spuštění aplikace

```bash
streamlit run app_secure.py
```

Aplikace se otevře na: `http://localhost:8501`

## Krok 4: Přihlášení

- Uživatelské jméno: hodnota z `APP_USERNAME`
- Heslo: hodnota z `APP_PASSWORD`

---

## ⚠️ Důležité bezpečnostní poznámky

1. **Nikdy nepoužívejte výchozí heslo** `change_me_in_production`
2. **Pro produkci vždy používejte HTTPS** (viz `DEPLOYMENT_SECURITY.md`)
3. **Nechtejte `.env` soubor do repozitáře**
4. **Pravidelně měňte hesla**

---

## Další informace

Pro detailní návod na nasazení v produkci viz: `DEPLOYMENT_SECURITY.md`




