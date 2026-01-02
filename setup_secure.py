"""
Pomocný skript pro nastavení bezpečné konfigurace aplikace
"""
import os
import secrets
import getpass
from pathlib import Path

def generate_secure_password(length=24):
    """Generuje bezpečné heslo"""
    return secrets.token_urlsafe(length)

def setup_config():
    """Interaktivní nastavení konfigurace"""
    print("=" * 60)
    print("Nastavení bezpečné konfigurace aplikace")
    print("=" * 60)
    print()
    
    # Uživatelské jméno
    username = input("Zadejte uživatelské jméno [admin]: ").strip() or "admin"
    
    # Heslo
    print("\nGenerování bezpečného hesla...")
    auto_password = generate_secure_password()
    print(f"Navržené heslo: {auto_password}")
    
    use_auto = input("\nPoužít navržené heslo? (y/n) [y]: ").strip().lower() or "y"
    
    if use_auto == "y":
        password = auto_password
    else:
        password = getpass.getpass("Zadejte vlastní heslo: ")
        if len(password) < 12:
            print("⚠️  Varování: Heslo by mělo mít alespoň 12 znaků")
            confirm = input("Pokračovat? (y/n): ").strip().lower()
            if confirm != "y":
                print("Zrušeno.")
                return
    
    # Další nastavení
    print("\n--- Další nastavení (Enter pro výchozí hodnoty) ---")
    max_file_size = input(f"Maximální velikost souboru v MB [50]: ").strip() or "50"
    max_files = input(f"Maximální počet souborů na session [20]: ").strip() or "20"
    session_timeout = input(f"Session timeout v sekundách [3600]: ").strip() or "3600"
    debug_mode = input(f"Debug mód (true/false) [false]: ").strip().lower() or "false"
    
    # Vytvoření .env souboru
    env_content = f"""# Bezpečnostní konfigurace aplikace
# Vygenerováno pomocí setup_secure.py

# ============================================================================
# AUTHENTICATION
# ============================================================================
APP_USERNAME={username}
APP_PASSWORD={password}

# ============================================================================
# FILE UPLOAD SECURITY
# ============================================================================
MAX_FILE_SIZE_MB={max_file_size}
MAX_FILES_PER_SESSION={max_files}

# ============================================================================
# APPLICATION SECURITY
# ============================================================================
REQUIRE_HTTPS=false
SESSION_TIMEOUT={session_timeout}
RATE_LIMIT_PER_MINUTE=30

# ============================================================================
# LOGGING
# ============================================================================
LOG_LEVEL=INFO
LOG_DIR=logs

# ============================================================================
# DEVELOPMENT
# ============================================================================
DEBUG_MODE={debug_mode}
"""
    
    env_path = Path(".env")
    
    if env_path.exists():
        overwrite = input(f"\nSoubor .env již existuje. Přepsat? (y/n) [n]: ").strip().lower() or "n"
        if overwrite != "y":
            print("Zrušeno.")
            return
    
    # Zápis do souboru
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    # Nastavení oprávnění (Unix)
    if os.name != "nt":
        os.chmod(env_path, 0o600)  # Read/write pouze pro vlastníka
    
    print("\n✅ Konfigurace úspěšně vytvořena!")
    print(f"📄 Soubor: {env_path.absolute()}")
    print("\n⚠️  DŮLEŽITÉ:")
    print("   - Uchovávejte .env soubor v bezpečí")
    print("   - Nikdy necommitněte .env do repozitáře")
    print("   - Pro produkci zvažte použití environment variables místo .env")
    print("\n🚀 Nyní můžete spustit aplikaci:")
    print("   streamlit run app_secure.py")

if __name__ == "__main__":
    try:
        setup_config()
    except KeyboardInterrupt:
        print("\n\nZrušeno uživatelem.")
    except Exception as e:
        print(f"\n❌ Chyba: {e}")




