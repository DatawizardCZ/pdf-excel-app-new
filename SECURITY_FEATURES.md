# 🔒 Přehled bezpečnostních funkcí

Tento dokument popisuje všechny bezpečnostní funkce implementované v `app_secure.py`.

## ✅ Implementované bezpečnostní funkce

### 1. Autentizace uživatelů
- **Přihlašovací systém**: Uživatelé se musí přihlásit před použitím aplikace
- **Session management**: Automatické odhlášení po timeout
- **Ochrana proti brute force**: Omezení počtu neúspěšných pokusů (5 pokusů)
- **Hashování hesel**: Hesla jsou hashována pomocí SHA-256 (v produkci použijte bcrypt/argon2)

### 2. Validace nahrávaných souborů
- **Kontrola typu souboru**: Pouze PDF soubory jsou povoleny
- **Kontrola velikosti**: Maximální velikost souboru (výchozí: 50 MB)
- **Kontrola PDF integrity**: Ověření, že soubor je platný PDF
- **Omezení počtu souborů**: Maximální počet souborů na session (výchozí: 20)
- **Sanitizace názvů souborů**: Odstranění nebezpečných znaků z názvů souborů

### 3. Bezpečná konfigurace
- **Environment variables**: Citlivá data (hesla) se ukládají jako environment variables
- **Podpora .env souborů**: Volitelné použití .env pro lokální vývoj
- **Konfigurovatelné limity**: Všechny limity jsou konfigurovatelné
- **Separace development/produkce**: Debug mód lze vypnout v produkci

### 4. Bezpečné zpracování chyb
- **Sanitizace chybových zpráv**: V produkci se nezobrazují detailní chyby
- **Bezpečné logování**: Chyby se logují, ale nezobrazují uživateli
- **Ochrana proti informačnímu úniku**: Uživatelé nevidí interní detaily systému

### 5. Logging a monitoring
- **Strukturované logování**: Všechny důležité události se logují
- **Sledování přihlášení**: Úspěšná i neúspěšná přihlášení
- **Sledování zpracování**: Zpracované soubory a chyby
- **Rotace logů**: Logy se ukládají do souboru s možností rotace

### 6. Správa dočasných souborů
- **Bezpečné názvy souborů**: Použití tokenů pro dočasné soubory
- **Automatické mazání**: Dočasné soubory se automaticky mažou po zpracování
- **Izolovaný adresář**: Dočasné soubory v samostatném adresáři

### 7. Session management
- **Timeout session**: Automatické odhlášení po určité době nečinnosti
- **Zobrazení zbývajícího času**: Uživatel vidí, kdy session vyprší
- **Možnost odhlášení**: Uživatel se může kdykoli odhlásit

## 📋 Konfigurovatelné parametry

Všechny parametry lze nastavit pomocí environment variables nebo .env souboru:

| Parametr | Výchozí hodnota | Popis |
|----------|----------------|-------|
| `APP_USERNAME` | `admin` | Uživatelské jméno pro přihlášení |
| `APP_PASSWORD` | `change_me_in_production` | Heslo pro přihlášení |
| `MAX_FILE_SIZE_MB` | `50` | Maximální velikost souboru v MB |
| `MAX_FILES_PER_SESSION` | `20` | Maximální počet souborů na session |
| `SESSION_TIMEOUT` | `3600` | Timeout session v sekundách (1 hodina) |
| `REQUIRE_HTTPS` | `false` | Vyžadovat HTTPS (nastavte na `true` v produkci) |
| `DEBUG_MODE` | `false` | Zobrazovat detailní chyby (nastavte na `false` v produkci) |
| `LOG_LEVEL` | `INFO` | Úroveň logování (DEBUG, INFO, WARNING, ERROR) |
| `LOG_DIR` | `logs` | Adresář pro logy |

## 🔐 Doporučení pro produkci

### Povinné změny před nasazením:

1. **Změňte výchozí přihlašovací údaje**
   ```bash
   export APP_USERNAME="bezpecne_uzivatelske_jmeno"
   export APP_PASSWORD="silne_heslo_min_12_znaku"
   ```

2. **Vypněte debug mód**
   ```bash
   export DEBUG_MODE="false"
   ```

3. **Použijte HTTPS**
   - Nastavte `REQUIRE_HTTPS=true`
   - Použijte reverse proxy (nginx, Apache) s SSL certifikátem

4. **Omezte přístup**
   - Použijte firewall pro omezení přístupu
   - Zvažte whitelist IP adres v nginx

5. **Nastavte rotaci logů**
   - Použijte logrotate pro správu log souborů
   - Pravidelně kontrolujte logy pro podezřelou aktivitu

### Volitelné vylepšení:

1. **Použijte bcrypt/argon2 pro hashování hesel**
   - Aktuálně se používá SHA-256, což je pro produkci méně bezpečné
   - Implementujte bcrypt nebo argon2 pro hashování hesel

2. **Přidejte vícefaktorovou autentizaci (MFA)**
   - Použijte TOTP (Time-based One-Time Password)
   - Nebo SMS/Email ověření

3. **Implementujte rate limiting**
   - Omezte počet požadavků z jedné IP adresy
   - Použijte nástroje jako Redis pro distribuci

4. **Přidejte audit log**
   - Sledujte všechny akce uživatelů
   - Ukládejte IP adresy a časové razítka

5. **Použijte databázi pro uživatele**
   - Místo hardcoded uživatelů použijte databázi
   - Implementujte správu uživatelů a rolí

## 📚 Další dokumentace

- `DEPLOYMENT_SECURITY.md` - Detailní návod na nasazení
- `QUICK_START_SECURE.md` - Rychlý start
- `setup_secure.py` - Interaktivní nastavení konfigurace

## ⚠️ Bezpečnostní upozornění

1. **Nikdy necommitněte `.env` soubor** do repozitáře
2. **Používejte silná hesla** (min. 12 znaků, kombinace znaků)
3. **Pravidelně aktualizujte závislosti** pro opravy bezpečnostních chyb
4. **Monitorujte logy** pro podezřelou aktivitu
5. **Používejte HTTPS** v produkci

---

**Verze:** 1.0  
**Poslední aktualizace:** 2025-11-07




