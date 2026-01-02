# 🔒 Bezpečnostní průvodce nasazením aplikace

Tento dokument popisuje kroky pro bezpečné nasazení aplikace v produkčním prostředí u jiné společnosti.

## 📋 Obsah

1. [Před nasazením](#před-nasazením)
2. [Konfigurace bezpečnosti](#konfigurace-bezpečnosti)
3. [Nasazení aplikace](#nasazení-aplikace)
4. [Bezpečnostní opatření](#bezpečnostní-opatření)
5. [Monitoring a logování](#monitoring-a-logování)
6. [Kontrolní seznam](#kontrolní-seznam)

---

## Před nasazením

### 1. Zkontrolujte závislosti

```bash
pip install -r requirements.txt
```

### 2. Vytvořte bezpečné přihlašovací údaje

**⚠️ DŮLEŽITÉ:** Nikdy nepoužívejte výchozí přihlašovací údaje v produkci!

---

## Konfigurace bezpečnosti

### Metoda 1: Environment Variables (Doporučeno)

#### Windows (PowerShell):
```powershell
$env:APP_USERNAME="bezpecne_uzivatelske_jmeno"
$env:APP_PASSWORD="silne_heslo_min_12_znaku"
$env:MAX_FILE_SIZE_MB="50"
$env:MAX_FILES_PER_SESSION="20"
$env:SESSION_TIMEOUT="3600"
$env:REQUIRE_HTTPS="true"
$env:DEBUG_MODE="false"
```

#### Linux/Mac:
```bash
export APP_USERNAME="bezpecne_uzivatelske_jmeno"
export APP_PASSWORD="silne_heslo_min_12_znaku"
export MAX_FILE_SIZE_MB="50"
export MAX_FILES_PER_SESSION="20"
export SESSION_TIMEOUT="3600"
export REQUIRE_HTTPS="true"
export DEBUG_MODE="false"
```

### Metoda 2: Soubor .env (Alternativa)

Vytvořte soubor `.env` v kořenovém adresáři projektu:

```env
APP_USERNAME=bezpecne_uzivatelske_jmeno
APP_PASSWORD=silne_heslo_min_12_znaku
MAX_FILE_SIZE_MB=50
MAX_FILES_PER_SESSION=20
SESSION_TIMEOUT=3600
REQUIRE_HTTPS=true
DEBUG_MODE=false
LOG_LEVEL=INFO
```

**⚠️ DŮLEŽITÉ:** 
- Přidejte `.env` do `.gitignore`
- Nikdy necommitněte `.env` do repozitáře
- Uchovávejte hesla v bezpečném správci hesel

### Metoda 3: Upravit config.py přímo (Nedoporučeno)

Pouze pro testování. V produkci vždy používejte environment variables.

---

## Nasazení aplikace

### Varianta A: Lokální nasazení (pro menší týmy)

#### 1. Instalace závislostí
```bash
pip install -r requirements.txt
```

#### 2. Nastavení environment variables (viz výše)

#### 3. Spuštění aplikace
```bash
streamlit run app_secure.py --server.port 8501
```

#### 4. Přístup
- Lokální: `http://localhost:8501`
- V síti: `http://[IP_ADRESA]:8501`

**⚠️ BEZPEČNOST:** Pro produkci vždy používejte HTTPS přes reverse proxy (nginx, Apache).

### Varianta B: Nasazení na serveru s HTTPS

#### 1. Instalace na serveru
```bash
# SSH na server
ssh user@server-address

# Klonování nebo nahrání souborů
cd /opt/darvis-pdf-app

# Instalace závislostí
pip3 install -r requirements.txt
```

#### 2. Konfigurace nginx (reverse proxy)

Vytvořte `/etc/nginx/sites-available/darvis-pdf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Přesměrování na HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL certifikáty (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL konfigurace
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout nastavení
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

Aktivujte konfiguraci:
```bash
sudo ln -s /etc/nginx/sites-available/darvis-pdf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. SSL certifikát (Let's Encrypt)
```bash
sudo certbot --nginx -d your-domain.com
```

#### 4. Spuštění jako systemd služba

Vytvořte `/etc/systemd/system/darvis-pdf.service`:

```ini
[Unit]
Description=Darvis PDF Processing App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/darvis-pdf-app
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="APP_USERNAME=your_username"
Environment="APP_PASSWORD=your_secure_password"
Environment="REQUIRE_HTTPS=true"
Environment="DEBUG_MODE=false"
ExecStart=/usr/local/bin/streamlit run app_secure.py --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktivujte službu:
```bash
sudo systemctl daemon-reload
sudo systemctl enable darvis-pdf
sudo systemctl start darvis-pdf
sudo systemctl status darvis-pdf
```

### Varianta C: Docker nasazení

Vytvořte `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app_secure.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Vytvořte `docker-compose.yml`:

```yaml
version: '3.8'

services:
  darvis-pdf:
    build: .
    ports:
      - "8501:8501"
    environment:
      - APP_USERNAME=${APP_USERNAME}
      - APP_PASSWORD=${APP_PASSWORD}
      - MAX_FILE_SIZE_MB=50
      - MAX_FILES_PER_SESSION=20
      - REQUIRE_HTTPS=false  # HTTPS řeší reverse proxy
      - DEBUG_MODE=false
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

Spuštění:
```bash
docker-compose up -d
```

---

## Bezpečnostní opatření

### 1. Silná hesla

**Požadavky na heslo:**
- Minimálně 12 znaků
- Kombinace velkých a malých písmen
- Čísla a speciální znaky
- Nepoužívejte běžná slova nebo osobní informace

**Generování bezpečného hesla:**
```bash
# Linux/Mac
openssl rand -base64 24

# Python
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

### 2. Firewall konfigurace

Omezte přístup pouze na potřebné porty:

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 3. Omezení přístupu podle IP

V nginx můžete přidat whitelist:

```nginx
location / {
    allow 192.168.1.0/24;  # Vaše síť
    allow 10.0.0.0/8;       # Interní síť
    deny all;
    
    proxy_pass http://127.0.0.1:8501;
    # ... zbytek konfigurace
}
```

### 4. Pravidelné aktualizace

```bash
# Aktualizace systému
sudo apt update && sudo apt upgrade -y

# Aktualizace Python balíčků
pip install --upgrade -r requirements.txt
```

### 5. Zálohování logů

Nastavte rotaci logů v `/etc/logrotate.d/darvis-pdf`:

```
/opt/darvis-pdf-app/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
}
```

---

## Monitoring a logování

### 1. Kontrola logů

```bash
# Zobrazení logů v reálném čase
tail -f logs/app.log

# Hledání chyb
grep ERROR logs/app.log

# Hledání neúspěšných přihlášení
grep "Neúspěšný pokus" logs/app.log
```

### 2. Monitoring přístupů

Aplikace automaticky loguje:
- Úspěšná a neúspěšná přihlášení
- Zpracované soubory
- Chyby při zpracování

### 3. Alerting (volitelné)

Můžete nastavit monitoring nástroje jako:
- **Prometheus + Grafana** pro metriky
- **Sentry** pro error tracking
- **ELK Stack** pro centralizované logování

---

## Kontrolní seznam před nasazením

### Konfigurace
- [ ] Změněno výchozí uživatelské jméno
- [ ] Nastaveno silné heslo (min. 12 znaků)
- [ ] Konfigurovány environment variables
- [ ] `DEBUG_MODE=false` v produkci
- [ ] `REQUIRE_HTTPS=true` (pokud je HTTPS dostupné)

### Bezpečnost
- [ ] Aplikace běží za HTTPS (nebo reverse proxy)
- [ ] Firewall správně nakonfigurován
- [ ] Omezen přístup podle IP (pokud je potřeba)
- [ ] Logy jsou bezpečně uloženy
- [ ] Dočasné soubory se automaticky mažou

### Nasazení
- [ ] Všechny závislosti nainstalovány
- [ ] Aplikace testována v produkčním prostředí
- [ ] Systemd služba nebo Docker kontejner běží
- [ ] Automatický restart při selhání
- [ ] Monitoring a alerting nastaven

### Dokumentace
- [ ] Uživatelé mají přístup k návodu
- [ ] Administrátor má přístup k tomuto dokumentu
- [ ] Kontaktní informace pro podporu

---

## Řešení problémů

### Aplikace se nespustí
1. Zkontrolujte logy: `journalctl -u darvis-pdf -n 50`
2. Ověřte environment variables: `env | grep APP_`
3. Zkontrolujte oprávnění souborů

### Uživatel se nemůže přihlásit
1. Ověřte správnost přihlašovacích údajů
2. Zkontrolujte logy pro neúspěšné pokusy
3. Ověřte, že session timeout není příliš krátký

### Chyby při zpracování PDF
1. Zkontrolujte velikost a formát souborů
2. Ověřte, že dočasný adresář má dostatek místa
3. Zkontrolujte logy pro detailní chyby

---

## Kontakt a podpora

Pro bezpečnostní problémy nebo dotazy kontaktujte administrátora systému.

**⚠️ DŮLEŽITÉ:** Při podezření na bezpečnostní incident:
1. Okamžitě odpojte aplikaci od sítě
2. Zkontrolujte logy
3. Změňte všechna hesla
4. Kontaktujte bezpečnostní tým

---

**Verze dokumentu:** 1.0  
**Poslední aktualizace:** 2025-11-07




