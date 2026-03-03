"""
Konfigurační modul pro bezpečnostní nastavení aplikace
Používá environment variables pro citlivá data
"""
import os
import tempfile
from pathlib import Path
from typing import List, Optional

# Načtení .env souboru pokud existuje (volitelné)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv není nainstalován, použijeme pouze environment variables
    pass

# ============================================================================
# AUTHENTICATION CONFIGURATION
# ============================================================================
# Pro produkci: Nastavte tyto hodnoty jako environment variables
# Windows: set APP_USERNAME=your_username
# Linux/Mac: export APP_USERNAME=your_username

APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "change_me_in_production")

# Alternativně: Použijte soubor .env (doporučeno)
# Vytvořte soubor .env v kořenovém adresáři s:
# APP_USERNAME=your_username
# APP_PASSWORD=your_secure_password

# ============================================================================
# FILE UPLOAD SECURITY
# ============================================================================
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))  # Maximální velikost souboru v MB
MAX_FILES_PER_SESSION = int(os.getenv("MAX_FILES_PER_SESSION", "20"))  # Maximální počet souborů
ALLOWED_FILE_TYPES = ['.pdf']  # Povolené typy souborů

# ============================================================================
# APPLICATION SECURITY
# ============================================================================
# Povolit pouze HTTPS v produkci
REQUIRE_HTTPS = os.getenv("REQUIRE_HTTPS", "false").lower() == "true"

# Session timeout v sekundách (výchozí: 1 hodina)
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))

# Rate limiting - maximální počet požadavků za minutu
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# Cesta k log souboru
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_FILE = LOG_DIR / "app.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR

# Vytvořit log adresář pokud neexistuje
LOG_DIR.mkdir(exist_ok=True)

# ============================================================================
# TEMPORARY FILES
# ============================================================================
# Adresář pro dočasné soubory (bude automaticky mazán)
TEMP_DIR = Path(os.getenv("TEMP_DIR", tempfile.gettempdir())) / "pdf_processor"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# ERROR HANDLING
# ============================================================================
# Zobrazovat detailní chyby pouze v development módu
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# ============================================================================
# APPLICATION METADATA
# ============================================================================
APP_NAME = "Darvis - PDF Objednávky"
APP_VERSION = "2.0.1"
APP_DESCRIPTION = "Bezpečná aplikace pro převod PDF objednávek do Excelu"

