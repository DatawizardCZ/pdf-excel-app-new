# PowerShell script to install dependencies and run the app
# Uses the correct Python path from Miniconda

$pythonPath = "$env:USERPROFILE\miniconda3\envs\pydata-book\python.exe"

Write-Host "`n🐍 Using Python: $pythonPath`n" -ForegroundColor Cyan

# Check if Python exists
if (-not (Test-Path $pythonPath)) {
    Write-Host "❌ Python not found at: $pythonPath" -ForegroundColor Red
    Write-Host "Please check your Miniconda installation." -ForegroundColor Yellow
    exit 1
}

# Show Python version
Write-Host "Python version:" -ForegroundColor Yellow
& $pythonPath --version
Write-Host ""

# Install dependencies
Write-Host "📦 Installing dependencies...`n" -ForegroundColor Cyan
& $pythonPath -m pip install streamlit pandas pdfplumber openpyxl python-dotenv

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Dependencies installed!`n" -ForegroundColor Green

# Check if app.py exists
if (-not (Test-Path "app.py")) {
    Write-Host "❌ app.py not found in current directory" -ForegroundColor Red
    Write-Host "Please navigate to the project directory first." -ForegroundColor Yellow
    exit 1
}

# Run the app
Write-Host "🚀 Starting Streamlit app...`n" -ForegroundColor Cyan
Write-Host "The app will open in your browser at http://localhost:8501`n" -ForegroundColor Yellow

& $pythonPath -m streamlit run app.py


