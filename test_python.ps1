# Quick script to find Python installations
Write-Host "`n🔍 Hledám Python instalace...`n" -ForegroundColor Cyan

$found = $false

# Common Python installation locations
$searchPaths = @(
    "C:\Python*",
    "$env:LOCALAPPDATA\Programs\Python\Python*",
    "$env:ProgramFiles\Python*",
    "$env:ProgramFiles(x86)\Python*",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python*"
)

foreach ($pattern in $searchPaths) {
    $dirs = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue -Directory
    foreach ($dir in $dirs) {
        $pythonExe = Join-Path $dir.FullName "python.exe"
        if (Test-Path $pythonExe) {
            $found = $true
            Write-Host "✅ NALEZENO!" -ForegroundColor Green
            Write-Host "   Cesta: $pythonExe" -ForegroundColor White
            try {
                $version = & $pythonExe --version 2>&1
                Write-Host "   Verze: $version" -ForegroundColor Cyan
            } catch {
                Write-Host "   (Nelze zjistit verzi)" -ForegroundColor Yellow
            }
            Write-Host ""
            Write-Host "💡 Můžete použít:" -ForegroundColor Yellow
            Write-Host "   '$pythonExe -m pip install -r requirements.txt'" -ForegroundColor Green
            Write-Host "   '$pythonExe -m streamlit run app.py'" -ForegroundColor Green
            Write-Host ""
        }
    }
}

if (-not $found) {
    Write-Host "❌ Python nebyl nalezen v běžných umístěních" -ForegroundColor Red
    Write-Host ""
    Write-Host "Možná řešení:" -ForegroundColor Yellow
    Write-Host "1. Zkontrolujte, zda je Python nainstalovaný" -ForegroundColor White
    Write-Host "2. Zkuste přeinstalovat Python z: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "3. Při instalaci ZAŠKRTNĚTE 'Add Python to PATH'" -ForegroundColor White
    Write-Host ""
}

Write-Host "Stiskněte Enter pro ukončení..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

