# ✅ Solution: Connection Refused Issue

## The Problem

Streamlit shows "Welcome" but browser can't connect because:
- **The app crashes when loading** due to missing `pdf_processor` module
- This happens because Streamlit is running from wrong directory

## The Fix

### Option 1: Use the Fixed Batch File (Easiest) ✅

**Double-click:** `START_APP_FIXED.bat`

This ensures:
- ✅ You're in the correct directory
- ✅ All files are found (app.py, pdf_processor.py)
- ✅ Python path is correct
- ✅ Streamlit starts from right location

### Option 2: Manual Fix in Terminal

1. **Open Cursor's terminal** (`` Ctrl + ` ``)

2. **Navigate to project directory:**
   ```powershell
   cd "C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky"
   ```

3. **Verify you're in right place:**
   ```powershell
   dir app.py
   dir pdf_processor.py
   ```
   Both should show the files.

4. **Start Streamlit:**
   ```powershell
   & "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
   ```

5. **Wait for this message:**
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

6. **Open browser** to `http://localhost:8501`

---

## Why This Happens

When you run `streamlit run app.py`, Python needs to:
1. Find `app.py` ✅
2. Import `pdf_processor` from same directory ❌ (fails if wrong directory)

If you're not in the project directory, Python can't find `pdf_processor.py`.

---

## Quick Test

Run this to verify everything works:

```powershell
# Navigate to project
cd "C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky"

# Test import
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -c "from pdf_processor import extract_data_from_pdf; print('OK')"

# If you see "OK", then start Streamlit
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
```

---

## Summary

**The issue:** Wrong working directory when starting Streamlit

**The solution:** 
1. Make sure you're in the project directory
2. Use `START_APP_FIXED.bat` (easiest)
3. Or navigate manually before running streamlit

**Try `START_APP_FIXED.bat` now!** It should work! 🚀


