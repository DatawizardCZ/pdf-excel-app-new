# 🔧 Fix Python PATH Issue

## Problem
Python is installed (in Miniconda) but not in PATH, so `python` command doesn't work in terminal.

## Solution Options

### Option 1: Use Full Path (Quick Fix) ✅

Instead of `python`, use the full path:

```powershell
# Install dependencies
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m pip install -r requirements.txt

# Run app
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
```

### Option 2: Add Python to PATH (Permanent Fix)

1. **Find Python path:**
   ```
   C:\Users\Ev\miniconda3\envs\pydata-book\python.exe
   ```
   The directory is: `C:\Users\Ev\miniconda3\envs\pydata-book\`

2. **Add to PATH:**
   - Press `Win + R`
   - Type: `sysdm.cpl` and press Enter
   - Click "Advanced" tab → "Environment Variables"
   - Under "User variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\Users\Ev\miniconda3\envs\pydata-book`
   - Click "New" and add: `C:\Users\Ev\miniconda3\envs\pydata-book\Scripts`
   - Click OK on all windows
   - **Restart terminal** (close and reopen)

3. **Test:**
   ```powershell
   python --version
   ```

### Option 3: Use Cursor's Terminal (Easiest!)

Cursor's integrated terminal might automatically use the Python you selected!

1. In Cursor, open terminal: `` Ctrl + ` ``
2. Try: `python --version`
3. If it works, you're done! 🎉

### Option 4: Create Alias (PowerShell)

Add this to your PowerShell profile:

```powershell
# Open profile
notepad $PROFILE

# Add this line:
Set-Alias python "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe"
```

Then restart terminal.

---

## Quick Commands (Use These Now)

Copy and paste these into Cursor's terminal:

```powershell
# Install dependencies
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m pip install streamlit pandas pdfplumber openpyxl python-dotenv

# Run the app
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
```

---

## Recommended: Use the Batch File

I created `START_APP_WITH_PYTHON.bat` - just double-click it!

It automatically uses the correct Python path.


