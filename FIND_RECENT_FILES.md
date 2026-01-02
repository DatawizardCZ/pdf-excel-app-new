# 🔍 How to Find Recently Worked Files

## Quick Methods

### Method 1: Using Git (Best for tracking changes)

```bash
# Files changed in last commit
git show --name-only

# Files changed in last 3 commits  
git log --name-only -3

# Files modified by you in last week
git log --since="7 days ago" --author="Your Name" --name-only --pretty=format:"%h - %ar : %s"

# All files changed in last 24 hours
git log --since="24 hours ago" --name-only --pretty=format:"%h - %an, %ar : %s"
```

### Method 2: Using PowerShell (Best for file timestamps)

```powershell
# Files modified today
Get-ChildItem -Recurse -File | 
    Where-Object { $_.LastWriteTime -gt (Get-Date).Date } | 
    Select-Object Name, LastWriteTime | 
    Sort-Object LastWriteTime -Descending

# Files modified in last 7 days
Get-ChildItem -Recurse -File | 
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) } | 
    Select-Object Name, LastWriteTime | 
    Sort-Object LastWriteTime -Descending

# Files created today
Get-ChildItem -Recurse -File | 
    Where-Object { $_.CreationTime -gt (Get-Date).Date } | 
    Select-Object Name, CreationTime | 
    Sort-Object CreationTime -Descending
```

### Method 3: Using File Explorer

1. Open File Explorer
2. Navigate to project folder
3. Click "Date modified" column header to sort
4. Recent files will be at top

### Method 4: Using VS Code/Cursor

1. Open Command Palette: `Ctrl+Shift+P`
2. Type: "File: Show Active File in Explorer"
3. Or use Timeline view (right sidebar) to see recent changes

---

## Recommended Approach

**Don't move files to date folders** - it messes with git history!

Instead:
1. ✅ Use `RECENT_WORK.md` to document what you worked on
2. ✅ Use git commands to see recent changes
3. ✅ Use file timestamps in PowerShell
4. ✅ Keep project structure standard (files in root or logical folders)

---

## Create a Quick Script

Save this as `find_recent.ps1`:

```powershell
# Find files modified in last N days
param([int]$Days = 1)

$cutoff = (Get-Date).AddDays(-$Days)
Get-ChildItem -Recurse -File | 
    Where-Object { $_.LastWriteTime -gt $cutoff } | 
    Select-Object Name, LastWriteTime, FullName | 
    Sort-Object LastWriteTime -Descending |
    Format-Table -AutoSize
```

Usage:
```powershell
.\find_recent.ps1        # Last 1 day
.\find_recent.ps1 -Days 7   # Last 7 days
```



