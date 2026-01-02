# 🐍 Simple Python Setup Guide

## If you can't find "Select Interpreter" in Cursor

Don't worry! Here are alternative ways to get Python working:

---

## Method 1: Find Python Location Manually

### Step 1: Check Common Locations

Open File Explorer and check these folders:

1. **`C:\Python3x\`** (where x is version number like 311, 312)
2. **`C:\Users\Ev\AppData\Local\Programs\Python\Python3x\`**
3. **`C:\Program Files\Python3x\`**

Look for a file called **`python.exe`** in these folders.

### Step 2: Test Python

Once you find `python.exe`, open PowerShell in the project folder and test it:

```powershell
# Replace with your actual path
C:\Python311\python.exe --version
```

If it shows a version (like `Python 3.11.5`), it works!

---

## Method 2: Use Full Path in Commands

Once you know where Python is, use the full path:

### Install dependencies:
```powershell
C:\Python311\python.exe -m pip install -r requirements.txt
```

### Run the app:
```powershell
C:\Python311\python.exe -m streamlit run app.py
```

---

## Method 3: Add Python to PATH (Permanent Solution)

### Windows 10/11:

1. **Find Python location** (from Method 1)

2. **Add to PATH:**
   - Press `Win + R`
   - Type: `sysdm.cpl`
   - Click "Advanced" tab
   - Click "Environment Variables"
   - Under "System variables", find `Path`
   - Click "Edit"
   - Click "New"
   - Add: `C:\Python311\` (your Python folder)
   - Add: `C:\Python311\Scripts\` (Scripts folder)
   - Click OK on all windows

3. **Restart terminal** (close and reopen PowerShell)

4. **Test:**
   ```powershell
   python --version
   ```

---

## Method 4: Create a Simple Batch File

Create a file `run_app.bat` with your Python path:

```batch
@echo off
C:\Python311\python.exe -m streamlit run app.py
pause
```

Replace `C:\Python311\` with your actual Python path.

---

## Method 5: Check Cursor Settings

In Cursor:

1. **Open Settings:**
   - `Ctrl + ,` (comma)
   - Or: File → Preferences → Settings

2. **Search for:** `python path`

3. **Set Python Path:**
   - Look for "Python: Default Interpreter Path"
   - Enter your Python path: `C:\Python311\python.exe`

---

## Quick Test Script

Save this as `test_python.ps1` and run it:

```powershell
# Test Python locations
$paths = @(
    "C:\Python*",
    "$env:LOCALAPPDATA\Programs\Python\Python*",
    "$env:ProgramFiles\Python*"
)

foreach ($pattern in $paths) {
    $dirs = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue -Directory
    foreach ($dir in $dirs) {
        $python = Join-Path $dir.FullName "python.exe"
        if (Test-Path $python) {
            Write-Host "✅ Found: $python" -ForegroundColor Green
            $version = & $python --version 2>&1
            Write-Host "   Version: $version" -ForegroundColor Cyan
            Write-Host ""
        }
    }
}
```

Run it:
```powershell
powershell -ExecutionPolicy Bypass -File .\test_python.ps1
```

---

## What to Do Right Now

1. **Try to find Python** using Method 1 (check common folders)
2. **Once found**, use the full path to run commands
3. **Or add to PATH** for permanent solution (Method 3)

---

## Still Can't Find Python?

### Reinstall Python:

1. Download from: https://www.python.org/downloads/
2. **IMPORTANT:** During installation, check ✅ **"Add Python to PATH"**
3. Complete installation
4. **Restart your computer**
5. Open new terminal and try: `python --version`

---

## Need Help?

Tell me:
- What folders you checked
- If you see any Python folders
- Any error messages you get

I'll help you find it! 🔍

