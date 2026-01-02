# ✅ Quick Start - Everything is Ready!

## 🎉 Success! Dependencies Installed

All packages are now installed:
- ✅ Streamlit
- ✅ Pandas  
- ✅ pdfplumber
- ✅ openpyxl
- ✅ python-dotenv

---

## 🚀 Run the App

### Method 1: Use the PowerShell Script (Easiest)

Double-click: **`install_and_run.ps1`**

This will:
1. Check Python
2. Install dependencies (if needed)
3. Start the app

### Method 2: Use the Batch File

Double-click: **`START_APP_WITH_PYTHON.bat`**

### Method 3: Manual Command

In Cursor's terminal, run:

```powershell
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
```

---

## 📝 What to Expect

1. **Terminal output:**
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

2. **Browser opens automatically** at `http://localhost:8501`

3. **You see the app interface:**
   - Upload PDF files
   - Click "Zpracovat objednávky"
   - Download Excel files

---

## 🔧 If Python Command Doesn't Work

Since `python` isn't in PATH, always use the full path:

```powershell
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" [command]
```

Examples:
```powershell
# Check version
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" --version

# Install package
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m pip install [package]

# Run script
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" script.py
```

---

## 💡 Tip: Add to PATH (Optional)

To use `python` directly, add to PATH:
1. `Win + R` → `sysdm.cpl`
2. Advanced → Environment Variables
3. Edit "Path" → Add: `C:\Users\Ev\miniconda3\envs\pydata-book`
4. Add: `C:\Users\Ev\miniconda3\envs\pydata-book\Scripts`
5. Restart terminal

---

## ✅ You're Ready!

The app should be starting now. Check your browser! 🎉


