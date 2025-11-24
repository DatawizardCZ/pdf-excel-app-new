"""
Bezpečná Streamlit aplikace pro převod PDF objednávek do Excelu
Darvis - PDF Objednávky (Secure Version)

Zabezpečení:
- Autentizace uživatelů
- Validace nahrávaných souborů
- Omezení velikosti a počtu souborů
- Bezpečné zpracování chyb
- Logging aktivit
- Session management
"""
import streamlit as st
import pandas as pd
import pdfplumber
from pathlib import Path
import io
import hashlib
import logging
import time
from datetime import datetime, timedelta
import re
import tempfile
import secrets
from typing import List, Dict, Optional, Tuple

from pdf_processor import extract_data_from_pdf
from config import (
    APP_USERNAME, APP_PASSWORD,
    MAX_FILE_SIZE_MB, MAX_FILES_PER_SESSION,
    ALLOWED_FILE_TYPES,
    SESSION_TIMEOUT,
    LOG_FILE, LOG_LEVEL,
    TEMP_DIR,
    DEBUG_MODE,
    APP_NAME, APP_VERSION
)

# ============================================================================
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.login_attempts = 0
    st.session_state.session_start = None
    st.session_state.upload_count = 0
    st.session_state.last_request_time = None

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================
def verify_password(username: str, password: str) -> bool:
    """Ověření uživatelského jména a hesla"""
    # V produkci: Použijte hashování hesel (bcrypt, argon2)
    # Pro jednoduchost zde používáme plain text (NEPOUŽÍVAT V PRODUKCI!)
    # Doporučeno: Použít streamlit-authenticator nebo vlastní hashování
    
    # Hashování pro bezpečnější porovnání
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    stored_hash = hashlib.sha256(APP_PASSWORD.encode()).hexdigest()
    
    is_valid = (username == APP_USERNAME and password_hash == stored_hash)
    
    if not is_valid:
        st.session_state.login_attempts += 1
        logger.warning(
            f"Neúspěšný pokus o přihlášení: {username} "
            f"(IP: {st.session_state.get('client_ip', 'unknown')})"
        )
    
    return is_valid

def check_session_timeout() -> bool:
    """Kontrola vypršení relace"""
    if not st.session_state.session_start:
        return False
    
    elapsed = time.time() - st.session_state.session_start
    return elapsed < SESSION_TIMEOUT

def login_page():
    """Zobrazí přihlašovací stránku"""
    # Konfigurace stránky
    st.set_page_config(
        page_title="Přihlášení",
        page_icon="🔐",
        layout="centered"
    )
    
    # Centrování přihlašovacího formuláře
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: center; margin-bottom: 0.5rem;'>🔐 Přihlášení</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: #666; margin-bottom: 2rem;'>PDF Objednávky</p>",
            unsafe_allow_html=True
        )
        
        # Varování při příliš mnoha pokusech
        if st.session_state.login_attempts >= 5:
            st.error("⚠️ Příliš mnoho neúspěšných pokusů. Zkuste to později.")
            st.stop()
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown("<div style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
            username = st.text_input(
                "Uživatelské jméno",
                key="login_username",
                placeholder="Zadejte uživatelské jméno"
            )
            password = st.text_input(
                "Heslo",
                type="password",
                key="login_password",
                placeholder="Zadejte heslo"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
            submit = st.form_submit_button(
                "Přihlásit se",
                type="primary",
                use_container_width=True
            )
            
            if submit:
                if verify_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.session_start = time.time()
                    st.session_state.login_attempts = 0
                    st.session_state.upload_count = 0
                    logger.info(f"Úspěšné přihlášení: {username}")
                    st.rerun()
                else:
                    st.error("❌ Neplatné uživatelské jméno nebo heslo")
                    logger.warning(f"Neúspěšný pokus o přihlášení (pokus {st.session_state.login_attempts + 1})")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align: center; color: #999; font-size: 0.85rem;'>{APP_NAME} v{APP_VERSION}</div>",
            unsafe_allow_html=True
        )

# ============================================================================
# FILE VALIDATION FUNCTIONS
# ============================================================================
def validate_file_type(filename: str) -> bool:
    """Ověření typu souboru"""
    file_ext = Path(filename).suffix.lower()
    return file_ext in ALLOWED_FILE_TYPES

def validate_file_size(file_size: int) -> bool:
    """Ověření velikosti souboru"""
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    return file_size <= max_size_bytes

def validate_pdf_file(file_bytes: bytes, filename: str) -> Tuple[bool, Optional[str]]:
    """Komplexní validace PDF souboru"""
    # Kontrola typu souboru
    if not validate_file_type(filename):
        return False, f"Neplatný typ souboru. Povolené typy: {', '.join(ALLOWED_FILE_TYPES)}"
    
    # Kontrola velikosti
    if not validate_file_size(len(file_bytes)):
        return False, f"Soubor je příliš velký. Maximální velikost: {MAX_FILE_SIZE_MB} MB"
    
    # Kontrola PDF hlavičky (magic bytes)
    pdf_signature = b'%PDF'
    if not file_bytes.startswith(pdf_signature):
        return False, "Soubor není platný PDF soubor"
    
    # Pokus o otevření PDF pro ověření integrity
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            if len(pdf.pages) == 0:
                return False, "PDF soubor neobsahuje žádné stránky"
    except Exception as e:
        logger.error(f"Chyba při validaci PDF {filename}: {str(e)}")
        return False, "PDF soubor je poškozený nebo neplatný"
    
    return True, None

# ============================================================================
# SECURITY HELPER FUNCTIONS
# ============================================================================
def sanitize_filename(filename: str) -> str:
    """Sanitizace názvu souboru pro bezpečné použití"""
    # Odstranit nebezpečné znaky
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Omezit délku
    if len(filename) > 255:
        name, ext = Path(filename).stem[:250], Path(filename).suffix
        filename = name + ext
    return filename

def sanitize_error_message(error: Exception) -> str:
    """Sanitizace chybových zpráv pro bezpečnost"""
    if DEBUG_MODE:
        return str(error)
    else:
        # V produkci zobrazit pouze obecnou chybovou zprávu
        return "Došlo k chybě při zpracování. Kontaktujte administrátora."


# ============================================================================
# DATA PROCESSING HELPERS
# ============================================================================
DESCRIPTION_ALIASES = ['description', 'beskrivelse']
SPECIFICATION_COLUMN = 'Specification'


def _split_description_text(value: str) -> Tuple[str, str]:
    """
    Rozdělí text popisu na první řádek (zůstává v Description) a druhý řádek
    (přesune se do samostatného sloupce Specification)
    """
    if value is None:
        return '', ''
    text = str(value)
    if not text:
        return '', ''

    lines = text.splitlines()
    if not lines:
        return text.strip(), ''

    first_line = lines[0].strip()
    second_line = lines[1].strip() if len(lines) > 1 else ''
    # Pokud je více řádků, zbytek spojíme do druhého řádku (uživatel chce celý zbytek v samostatném sloupci)
    if len(lines) > 2:
        remaining = '\n'.join(line.strip() for line in lines[1:] if line.strip())
        second_line = remaining

    return first_line, second_line


def _find_description_column(df: pd.DataFrame) -> Optional[str]:
    for col in df.columns:
        if col and col.strip().lower() in DESCRIPTION_ALIASES:
            return col
    return None


def prepare_dataframe_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    """
    Zajistí, že Excel bude přesně odpovídat tabulce v PDF:
    - Description obsahuje pouze první řádek textu
    - Druhý řádek se přesouvá do samostatného sloupce Specification
    - Sloupce jsou seřazeny tak, aby Specification následoval hned po Description
    """
    if df is None or df.empty:
        return df

    prepared_df = df.copy()
    description_col = _find_description_column(prepared_df)

    if description_col:
        desc_series = prepared_df[description_col].fillna('').astype(str)
        first_lines: List[str] = []
        second_lines: List[str] = []

        for text in desc_series:
            first, second = _split_description_text(text)
            first_lines.append(first)
            second_lines.append(second)

        prepared_df[description_col] = first_lines

        if SPECIFICATION_COLUMN not in prepared_df.columns:
            prepared_df[SPECIFICATION_COLUMN] = ''

        spec_series = prepared_df[SPECIFICATION_COLUMN].fillna('').astype(str)
        second_series = pd.Series(second_lines, index=prepared_df.index)
        needs_update = (spec_series.str.strip() == '') & (second_series.str.strip() != '')
        prepared_df.loc[needs_update, SPECIFICATION_COLUMN] = second_series[needs_update]

        # Přesunout sloupec Specification hned za Description/Beskrivelse
        if SPECIFICATION_COLUMN in prepared_df.columns:
            column_order = []
            for col in prepared_df.columns:
                if col == SPECIFICATION_COLUMN:
                    continue
                column_order.append(col)
                if col == description_col:
                    column_order.append(SPECIFICATION_COLUMN)
            if SPECIFICATION_COLUMN not in column_order:
                column_order.append(SPECIFICATION_COLUMN)
            prepared_df = prepared_df[column_order]

    # Odstranit sloupec "Variant" (je často prázdný)
    if 'Variant' in prepared_df.columns:
        prepared_df = prepared_df.drop(columns=['Variant'])

    return prepared_df

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main_app():
    """Hlavní aplikace (zobrazí se po přihlášení)"""
    # Kontrola session timeout
    if not check_session_timeout():
        st.session_state.authenticated = False
        st.error("⏱️ Vaše relace vypršela. Prosím, přihlaste se znovu.")
        st.rerun()
    
    # Konfigurace stránky
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header s informacemi o session
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Převod PDF objednávek do Excelu")
    with col2:
        if st.button("🚪 Odhlásit se"):
            st.session_state.authenticated = False
            st.session_state.session_start = None
            logger.info("Uživatel se odhlásil")
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar s instrukcemi a informacemi
    with st.sidebar:
        st.header("📋 Návod")
        st.markdown("""
        **Postup:**
        1. Nahrajte PDF soubory s objednávkami
        2. Klikněte na tlačítko "Zpracovat objednávky"
        3. Stáhněte si vygenerované Excel soubory
        
        **Očekávaný formát PDF:**  
        `Købsrekvisition [číslo] [zkratka].pdf`
        """)
        
        st.divider()
        
        st.subheader("ℹ️ Informace")
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("Max. velikost", f"{MAX_FILE_SIZE_MB} MB")
        with info_col2:
            st.metric("Max. souborů", MAX_FILES_PER_SESSION)
        
        # Informace o relaci
        if st.session_state.session_start:
            elapsed = time.time() - st.session_state.session_start
            remaining = SESSION_TIMEOUT - elapsed
            if remaining > 0:
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                st.divider()
                st.markdown("**⏱️ Čas do vypršení relace**")
                if minutes > 0:
                    st.info(f"{minutes} min {seconds} s")
                else:
                    st.warning(f"{seconds} s")
    
    # Hlavní obsah
    st.markdown("### 📤 Nahrání souborů")
    uploaded_files = st.file_uploader(
        "Vyberte PDF soubory s objednávkami",
        type=['pdf'],
        accept_multiple_files=True,
        help="Můžete nahrát více souborů najednou"
    )
    
    if uploaded_files:
        # Validace počtu souborů
        if len(uploaded_files) > MAX_FILES_PER_SESSION:
            st.error(f"❌ Příliš mnoho souborů. Maximum je {MAX_FILES_PER_SESSION} souborů.")
            st.stop()
        
        # Validace všech souborů před zpracováním
        validation_errors = []
        validated_files = []
        
        with st.spinner("Kontroluji nahrané soubory..."):
            for file in uploaded_files:
                file_bytes = file.read()
                file.seek(0)  # Reset pro pozdější použití
                
                is_valid, error_msg = validate_pdf_file(file_bytes, file.name)
                if is_valid:
                    validated_files.append(file)
                else:
                    validation_errors.append({
                        'file': file.name,
                        'error': error_msg
                    })
        
        if validation_errors:
            st.warning(f"⚠️ {len(validation_errors)} souborů neprošlo validací:")
            with st.expander("🔍 Zobrazit detaily chyb", expanded=True):
                for error in validation_errors:
                    st.error(f"**{error['file']}**  \n{error['error']}")
        
        if validated_files:
            st.success(f"✅ Načteno {len(validated_files)} platných souborů")
            
            # Zobrazení seznamu souborů
            with st.expander("📁 Seznam nahraných souborů"):
                for file in validated_files:
                    file_size_mb = len(file.read()) / (1024 * 1024)
                    file.seek(0)
                    st.write(f"- {file.name} ({file_size_mb:.2f} MB)")
            
            # Tlačítko pro zpracování
            if st.button("🔄 Zpracovat objednávky", type="primary", use_container_width=True):
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                processed_files = []
                errors = []
                
                for idx, uploaded_file in enumerate(validated_files):
                    try:
                        # Aktualizace progress baru
                        progress = (idx + 1) / len(validated_files)
                        progress_bar.progress(progress)
                        status_text.text(f"Zpracovávám: {uploaded_file.name} ({idx + 1}/{len(validated_files)})")
                        
                        # Zpracování PDF
                        pdf_bytes = uploaded_file.read()
                        
                        # Validace před zpracováním
                        is_valid, error_msg = validate_pdf_file(pdf_bytes, uploaded_file.name)
                        if not is_valid:
                            errors.append({
                                'file': uploaded_file.name,
                                'error': error_msg
                            })
                            continue
                        
                        # Uložit dočasně do souboru s bezpečným názvem
                        safe_filename = sanitize_filename(uploaded_file.name)
                        tmp_path = TEMP_DIR / f"{secrets.token_hex(8)}_{safe_filename}"
                        
                        try:
                            # Zápis do dočasného souboru
                            with open(tmp_path, 'wb') as tmp_file:
                                tmp_file.write(pdf_bytes)
                            
                            # Extrakce dat z PDF pomocí pdf_processor
                            df = extract_data_from_pdf(tmp_path)
                            df = prepare_dataframe_for_excel(df)
                            
                            # Generování názvu Excel souboru
                            pdf_name = Path(uploaded_file.name).stem
                            excel_name = sanitize_filename(f"{pdf_name}_processed.xlsx")
                            
                            # Uložení do Excelu v paměti
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name='Objednávka')
                            
                            excel_buffer.seek(0)
                            processed_files.append({
                                'name': excel_name,
                                'data': excel_buffer.getvalue()
                            })
                            
                            logger.info(f"Úspěšně zpracován soubor: {uploaded_file.name}")
                            
                        except Exception as e:
                            error_msg = sanitize_error_message(e)
                            errors.append({
                                'file': uploaded_file.name,
                                'error': error_msg
                            })
                            logger.error(f"Chyba při zpracování {uploaded_file.name}: {str(e)}", exc_info=True)
                        
                        finally:
                            # Smazat dočasný soubor
                            if tmp_path.exists():
                                try:
                                    tmp_path.unlink()
                                except Exception as e:
                                    logger.warning(f"Nepodařilo se smazat dočasný soubor {tmp_path}: {str(e)}")
                    
                    except Exception as e:
                        error_msg = sanitize_error_message(e)
                        errors.append({
                            'file': uploaded_file.name,
                            'error': error_msg
                        })
                        logger.error(f"Neočekávaná chyba při zpracování {uploaded_file.name}: {str(e)}", exc_info=True)
                
                    progress_bar.progress(1.0)
                    status_text.text("✅ Zpracování dokončeno!")
                    
                    # Zobrazení výsledků
                    if processed_files:
                        st.success(f"✅ Úspěšně zpracováno {len(processed_files)} souborů")
                        
                        st.markdown("### 📥 Stáhnout Excel soubory")
                        
                        # Zobrazení tlačítek pro stažení
                        cols = st.columns(min(3, len(processed_files)))
                        for idx, file_info in enumerate(processed_files):
                            with cols[idx % len(cols)]:
                                st.download_button(
                                    label=f"⬇️ {file_info['name']}",
                                    data=file_info['data'],
                                    file_name=file_info['name'],
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                        
                        # Hromadné stažení (ZIP)
                        if len(processed_files) > 1:
                            st.markdown("---")
                            st.info("💡 Tip: Pro stažení všech souborů najednou použijte jednotlivá tlačítka výše")
                    
                    if errors:
                        st.warning(f"⚠️ {len(errors)} souborů se nepodařilo zpracovat")
                        with st.expander("🔍 Detaily chyb"):
                            for error in errors:
                                st.error(f"**{error['file']}:** {error['error']}")
                    
                    # Aktualizace počítadla
                    st.session_state.upload_count += len(validated_files)
    
    else:
        st.info("👆 Nahrajte PDF soubory výše pro začátek")
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #666;'>{APP_NAME} | Verze {APP_VERSION}</div>",
        unsafe_allow_html=True
    )

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def main():
    """Hlavní vstupní bod aplikace"""
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()

