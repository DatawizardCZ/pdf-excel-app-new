# 🚀 How to Run the App with Your Python

## You Have Python 3.10.6 in Miniconda! ✅

Since `python` command doesn't work in terminal, use the **full path**:

---

## Quick Start

### Step 1: Install Dependencies

```powershell
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m pip install -r requirements.txt
```

### Step 2: Run the App

```powershell
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
```

---

## Easier: Create a Shortcut

I'll create a simple batch file that uses the correct Python path.

Or you can use Cursor's built-in terminal - it should automatically use the Python you selected!

---

## Try This Now

1. **In Cursor's terminal** (the one at the bottom), try:
   ```powershell
   python --version
   ```

2. **If that works**, great! Then:
   ```powershell
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```

3. **If it doesn't work**, use the full path commands above.

---

## Alternative: Use Cursor's Run Button

1. Open `app.py`
2. Look for a "Run" button or play icon
3. Cursor might be able to run it directly using the Python you selected!

---

**Try `python --version` in Cursor's terminal first** - it might work there even if it doesn't in PowerShell!


