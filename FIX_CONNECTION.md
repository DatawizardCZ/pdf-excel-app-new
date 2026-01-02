# 🔧 Fix "Localhost odmítl připojení" (Connection Refused)

## Problem
The browser shows "Connection refused" when trying to access `http://localhost:8501`

## Solutions

### Solution 1: Wait a Few Seconds ⏱️

Streamlit needs a few seconds to start. Try:
1. Wait 5-10 seconds after running the command
2. Refresh the browser (F5)
3. Try again

### Solution 2: Check if App is Running

In terminal, check:
```powershell
netstat -ano | findstr :8501
```

If you see output, the app is running. If not, it didn't start.

### Solution 3: Start the App Manually

**In Cursor's terminal** (bottom panel), run:

```powershell
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
```

**Wait for this message:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Then** open your browser to `http://localhost:8501`

### Solution 4: Use the Batch File

Double-click: **`START_APP_SIMPLE.bat`**

This will:
- Check Python exists
- Check app.py exists  
- Start the app
- Keep the window open so you can see errors

### Solution 5: Check for Errors

Look at the terminal output. Common errors:

**Error: "No module named 'streamlit'"**
```powershell
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m pip install streamlit
```

**Error: "Port 8501 is already in use"**
```powershell
# Use different port
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py --server.port 8502
# Then open: http://localhost:8502
```

**Error: "app.py not found"**
- Make sure you're in the project directory
- Check that `app.py` exists

### Solution 6: Check Firewall

Windows Firewall might be blocking:
1. Open Windows Defender Firewall
2. Allow Python/Streamlit through firewall
3. Or temporarily disable firewall to test

---

## Step-by-Step: Start App Correctly

1. **Open Cursor's terminal** (`` Ctrl + ` `` or View → Terminal)

2. **Navigate to project** (if not already there):
   ```powershell
   cd "C:\Users\Ev\Datawizard\Hub - Dokumenty\01_Projekty\2025-11 Darvis-PDF-Objednávky"
   ```

3. **Start the app:**
   ```powershell
   & "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m streamlit run app.py
   ```

4. **Wait for this message:**
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

5. **Open browser** to `http://localhost:8501`

6. **Keep terminal open** - if you close it, the app stops!

---

## Quick Test

Run this to check everything:

```powershell
# Check Python
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" --version

# Check Streamlit
& "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe" -m pip show streamlit

# Check app.py exists
Test-Path app.py
```

All should return success!

---

## Most Common Issue

**The terminal window was closed!** 

Streamlit runs in the terminal. If you close the terminal, the app stops.

**Solution:** Keep the terminal window open while using the app.

---

**Try starting the app again in Cursor's terminal and wait for the "Local URL" message!**


