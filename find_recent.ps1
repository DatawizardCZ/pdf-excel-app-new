# Find recently modified files
# Usage: .\find_recent.ps1 [-Days 7]

param(
    [int]$Days = 1,
    [switch]$Created,
    [switch]$Modified
)

$cutoff = (Get-Date).AddDays(-$Days)

Write-Host "`n🔍 Hledám soubory " -NoNewline
if ($Created) {
    Write-Host "vytvořené " -NoNewline -ForegroundColor Cyan
} elseif ($Modified) {
    Write-Host "upravené " -NoNewline -ForegroundColor Yellow
} else {
    Write-Host "upravené " -NoNewline -ForegroundColor Yellow
}
Write-Host "v posledních $Days dnech...`n" -ForegroundColor Green

$files = if ($Created) {
    Get-ChildItem -Recurse -File | 
        Where-Object { $_.CreationTime -gt $cutoff }
} else {
    Get-ChildItem -Recurse -File | 
        Where-Object { $_.LastWriteTime -gt $cutoff }
}

if ($files) {
    $files | 
        Select-Object Name, @{Name="Type";Expression={$_.Extension}}, 
                     @{Name="Modified";Expression={$_.LastWriteTime.ToString("yyyy-MM-dd HH:mm")}},
                     @{Name="Size";Expression={"{0:N0} KB" -f ($_.Length/1KB)}} | 
        Sort-Object Modified -Descending |
        Format-Table -AutoSize
    
    Write-Host "✅ Nalezeno $($files.Count) souborů" -ForegroundColor Green
} else {
    Write-Host "❌ Žádné soubory nenalezeny" -ForegroundColor Red
}

Write-Host ""



