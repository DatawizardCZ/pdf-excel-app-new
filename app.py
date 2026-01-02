"""
Streamlit aplikace pro převod PDF objednávek do Excelu
Darvis - PDF Objednávky
"""

import streamlit as st
import pandas as pd
import pdfplumber
from pathlib import Path
import io
from datetime import datetime
import re
import tempfile
from pdf_processor import extract_data_from_pdf

# Konfigurace stránky
st.set_page_config(
    page_title="Darvis - PDF Objednávky",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Převod PDF objednávek do Excelu")
st.markdown("---")

# Sidebar s instrukcemi
with st.sidebar:
    st.header("📋 Instrukce")
    st.markdown("""
    1. Nahrajte PDF soubory s objednávkami
    2. Klikněte na tlačítko "Zpracovat objednávky"
    3. Stáhněte si vygenerované Excel soubory
    
    **Formát PDF:** `Købsrekvisition [číslo] [zkratka].pdf`
    """)
    
    st.markdown("---")
    st.markdown("**Verze:** 1.0")

# Hlavní obsah
uploaded_files = st.file_uploader(
    "Vyberte PDF soubory s objednávkami",
    type=['pdf'],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ Načteno {len(uploaded_files)} souborů")
    
    # Zobrazení seznamu souborů
    with st.expander("📁 Seznam nahraných souborů"):
        for file in uploaded_files:
            st.write(f"- {file.name}")
    
    # Tlačítko pro zpracování
    if st.button("🔄 Zpracovat objednávky", type="primary", use_container_width=True):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        processed_files = []
        errors = []
        
        for idx, uploaded_file in enumerate(uploaded_files):
            try:
                # Aktualizace progress baru
                progress = (idx + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Zpracovávám: {uploaded_file.name} ({idx + 1}/{len(uploaded_files)})")
                
                # Zpracování PDF
                pdf_bytes = uploaded_file.read()
                
                # Uložit dočasně do souboru (pdf_processor potřebuje Path)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(pdf_bytes)
                    tmp_path = Path(tmp_file.name)
                
                try:
                    # Extrakce dat z PDF pomocí pdf_processor
                    df = extract_data_from_pdf(tmp_path)
                    
                    # Generování názvu Excel souboru
                    pdf_name = Path(uploaded_file.name).stem
                    excel_name = f"{pdf_name}_processed.xlsx"
                    
                    # Uložení do Excelu v paměti
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Objednávka')
                    
                    excel_buffer.seek(0)
                    processed_files.append({
                        'name': excel_name,
                        'data': excel_buffer.getvalue()
                    })
                    
                finally:
                    # Smazat dočasný soubor
                    if tmp_path.exists():
                        tmp_path.unlink()
                    
            except Exception as e:
                errors.append({
                    'file': uploaded_file.name,
                    'error': str(e)
                })
                st.error(f"❌ Chyba při zpracování {uploaded_file.name}: {str(e)}")
        
        progress_bar.progress(1.0)
        status_text.text("✅ Zpracování dokončeno!")
        
        # Zobrazení výsledků
        if processed_files:
            st.success(f"✅ Úspěšně zpracováno {len(processed_files)} souborů")
            
            # Zobrazit náhled dat
            if len(processed_files) > 0:
                with st.expander("📊 Náhled zpracovaných dat", expanded=False):
                    # Znovu načíst první soubor pro náhled
                    # (v produkci bychom měli data uložit v session state)
                    st.info("Náhled bude zobrazen po dokončení implementace")
            
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

else:
    st.info("👆 Nahrajte PDF soubory výše pro začátek")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Darvis - PDF Objednávky | Verze 1.0</div>",
    unsafe_allow_html=True
)

