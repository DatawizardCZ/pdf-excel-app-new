# Script to help find and select Python interpreter
# Usage: .\select_python.ps1

Write-Host "`n🐍 Hledám Python instalace...`n" -ForegroundColor Cyan

$pythonPaths = @()

# Common Python installation locations
$searchPaths = @(
    "C:\Python*",
    "$env:LOCALAPPDATA\Programs\Python\Python*",
    "$env:ProgramFiles\Python*",
    "$env:ProgramFiles(x86)\Python*",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python*"
)

Write-Host "Kontroluji běžná umístění...`n" -ForegroundColor Yellow

foreach ($pattern in $searchPaths) {
    $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue -Directory
    foreach ($dir in $found) {
        $pythonExe = Join-Path $dir.FullName "python.exe"
        if (Test-Path $pythonExe) {
            $version = & $pythonExe --version 2>&1
            $pythonPaths += [PSCustomObject]@{
                Path = $pythonExe
                Version = $version
                Directory = $dir.FullName
            }
            Write-Host "✅ Nalezeno: $version" -ForegroundColor Green
            Write-Host "   Cesta: $pythonExe`n" -ForegroundColor Gray
        }
    }
}

# Check Windows Store Python
$storePython = Get-Command python -ErrorAction SilentlyContinue
if ($storePython) {
    Write-Host "✅ Windows Store Python: $($storePython.Source)" -ForegroundColor Green
    $pythonPaths += [PSCustomObject]@{
        Path = $storePython.Source
        Version = "Windows Store"
        Directory = Split-Path $storePython.Source
    }
}

if ($pythonPaths.Count -eq 0) {
    Write-Host "`n❌ Python nebyl nalezen!" -ForegroundColor Red
    Write-Host "`nMožná řešení:" -ForegroundColor Yellow
    Write-Host "1. Nainstalujte Python z: https://www.python.org/downloads/"
    Write-Host "2. Při instalaci zaškrtněte 'Add Python to PATH'"
    Write-Host "3. Restartujte terminál nebo počítač`n"
    exit 1
}

Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "Nalezené Python instalace:" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan
Write-Host ""

for ($i = 0; $i -lt $pythonPaths.Count; $i++) {
    $p = $pythonPaths[$i]
    Write-Host "[$($i+1)] $($p.Version)" -ForegroundColor White
    Write-Host "    $($p.Path)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "`n💡 Pro použití v Cursor/VS Code:" -ForegroundColor Yellow
Write-Host "1. Stiskněte Ctrl+Shift+P"
Write-Host "2. Zadejte: 'Python: Select Interpreter'"
Write-Host "3. Vyberte nebo zadejte cestu k Pythonu`n"

Write-Host "💡 Pro použití v terminálu:" -ForegroundColor Yellow
Write-Host "Použijte plnou cestu, např.:" -ForegroundColor White
Write-Host "  '$($pythonPaths[0].Path) --version'" -ForegroundColor Green
Write-Host "  '$($pythonPaths[0].Path) -m pip install streamlit'" -ForegroundColor Green
Write-Host ""

# Test first Python
if ($pythonPaths.Count -gt 0) {
    $firstPython = $pythonPaths[0].Path
    Write-Host "🧪 Testuji první Python instalaci..." -ForegroundColor Cyan
    try {
        $test = & $firstPython --version 2>&1
        Write-Host "✅ Funguje: $test" -ForegroundColor Green
        Write-Host "`nMůžete použít:" -ForegroundColor Yellow
        Write-Host "  '$firstPython -m streamlit run app.py'" -ForegroundColor Green
    } catch {
        Write-Host "❌ Chyba při testování" -ForegroundColor Red
    }
}

Write-Host ""



