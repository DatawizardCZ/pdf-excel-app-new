# 🔍 Finding Python Installed by Cursor

## Where Cursor Usually Installs Python

Cursor typically installs Python in one of these locations:

1. **User AppData (Most Common):**
   - `C:\Users\Ev\AppData\Local\Programs\Python\`
   - `C:\Users\Ev\AppData\Local\Microsoft\WindowsApps\` (Windows Store version)

2. **Cursor's own directory:**
   - `C:\Users\Ev\AppData\Local\Programs\Cursor\`
   - Or in Cursor's extensions folder

3. **System-wide:**
   - `C:\Program Files\Python\`
   - `C:\Python\`

---

## Quick Check Methods

### Method 1: Check Cursor Settings

1. Open Cursor
2. Go to **File → Preferences → Settings** (or `Ctrl + ,`)
3. Search for: `python path`
4. Look for "Python: Default Interpreter Path" or similar setting
5. This will show you the path Cursor is using

### Method 2: Check Cursor's Python Extension

1. In Cursor, open Command Palette: `Ctrl + Shift + P`
2. Type: `Python: Show Installed Interpreters`
3. This should list all Python installations

### Method 3: Check Bottom Status Bar

1. Look at the bottom-right of Cursor window
2. You might see Python version displayed
3. Click on it to select/change interpreter

### Method 4: Check Settings JSON

1. Press `Ctrl + Shift + P`
2. Type: `Preferences: Open User Settings (JSON)`
3. Look for `python.defaultInterpreterPath` or `python.pythonPath`

---

## Manual Search

Run this PowerShell command to search common locations:

```powershell
$searchPaths = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:USERPROFILE\AppData\Local\Programs\Python",
    "C:\Python*",
    "C:\Program Files\Python*",
    "$env:LOCALAPPDATA\Programs\Cursor"
)

foreach ($path in $searchPaths) {
    $found = Get-ChildItem -Path $path -Recurse -Filter "python.exe" -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host "✅ Found: $($found.FullName)" -ForegroundColor Green
    }
}
```

---

## If Python Was Installed via Windows Store

If Cursor installed Python from Windows Store:

1. It's usually at: `C:\Users\Ev\AppData\Local\Microsoft\WindowsApps\`
2. But this is just a stub - real Python might be elsewhere
3. Check: `C:\Users\Ev\AppData\Local\Programs\Python\` for actual installation

---

## Quick Test

Try running Python directly:

```powershell
# Try these commands:
python --version
python3 --version
py --version

# If none work, Python might not be in PATH
# But Cursor can still use it if it knows the path
```

---

## Solution: Let Cursor Find It Automatically

1. **Open any Python file** (like `app.py`)
2. Cursor should automatically detect Python
3. Look at the bottom-right corner - you should see Python version
4. Click on it to see/change interpreter

---

## Alternative: Install Python Manually

If you can't find Cursor's Python:

1. Download from: https://www.python.org/downloads/
2. During installation, check **"Add Python to PATH"**
3. Restart Cursor
4. It should be detected automatically

---

## Next Steps

Once you find Python:

1. Note the full path (e.g., `C:\Users\Ev\AppData\Local\Programs\Python\Python311\python.exe`)
2. You can use this path directly in terminal:
   ```powershell
   C:\Users\Ev\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r requirements.txt
   ```
3. Or add it to PATH (see NEXT_STEPS.md)

---

**Tip:** The easiest way is to open `app.py` in Cursor and check the bottom-right status bar for Python version!


