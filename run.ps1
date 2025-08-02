# Excel Database Search Tool - PowerShell Launcher
# Handles Unicode filenames properly

# Set UTF-8 encoding for Unicode support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              🔍 EXCEL DATABASE SEARCH TOOL              ║" -ForegroundColor Cyan
Write-Host "║                Fast • Powerful • Unicode Ready          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Please install Python 3.6+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check for Unicode filename support
Write-Host "🌐 Unicode filename support: ✅ Enabled" -ForegroundColor Green
Write-Host "   Example: نتيجة الثانوية العامة 2025.xlsx" -ForegroundColor Cyan
Write-Host ""

# Check dependencies
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$requiredPackages = @("pandas", "openpyxl", "xlrd")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    try {
        python -c "import $package" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ $package" -ForegroundColor Green
        } else {
            $missingPackages += $package
            Write-Host "   ❌ $package (missing)" -ForegroundColor Red
        }
    } catch {
        $missingPackages += $package
        Write-Host "   ❌ $package (missing)" -ForegroundColor Red
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Missing packages detected. Installing..." -ForegroundColor Yellow
    $packagesString = $missingPackages -join " "
    python -m pip install $packagesString
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Packages installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install packages. Please run manually:" -ForegroundColor Red
        Write-Host "   pip install $packagesString" -ForegroundColor Yellow
        Read-Host "Press Enter to continue anyway"
    }
}

Write-Host ""
Write-Host "🚀 Starting Excel Database Search Tool..." -ForegroundColor Green
Write-Host ""

# Run the main application
try {
    python main.py
} catch {
    Write-Host ""
    Write-Host "❌ Error running application: $($_.Exception.Message)" -ForegroundColor Red
}

# Keep window open
Write-Host ""
Read-Host "Press Enter to exit"
