# Vercel Deployment Readiness Checker for Django BookMySeat

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "Vercel Deployment Readiness Checker" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

$allChecks = $true

# Check 1: Git initialized
Write-Host "[Checking] Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "[PASS] Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "[WARN] Git not initialized. Run: git init" -ForegroundColor Red
    $allChecks = $false
}

# Check 2: Required files exist
$requiredFiles = @(
    "requirements.txt",
    "vercel.json",
    "build_files.sh",
    ".gitignore",
    "manage.py",
    "bookmyseat/settings.py",
    "bookmyseat/wsgi.py"
)

Write-Host "`n[Checking] Required files..." -ForegroundColor Yellow
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "[PASS] $file exists" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $file missing" -ForegroundColor Red
        $allChecks = $false
    }
}

# Check 3: Verify requirements.txt has key dependencies
Write-Host "`n[Checking] Required dependencies..." -ForegroundColor Yellow
$requirements = Get-Content "requirements.txt" -Raw
$dependencies = @("Django", "dj-database-url", "psycopg2-binary", "gunicorn")

foreach ($dep in $dependencies) {
    if ($requirements -match $dep) {
        Write-Host "[PASS] $dep found in requirements.txt" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $dep missing from requirements.txt" -ForegroundColor Red
        $allChecks = $false
    }
}

# Check 4: Verify vercel.json configuration
Write-Host "`n[Checking] Vercel configuration..." -ForegroundColor Yellow
if (Test-Path "vercel.json") {
    $vercelConfig = Get-Content "vercel.json" -Raw
    if ($vercelConfig -match "python") {
        Write-Host "[PASS] Python runtime configured" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Python runtime not configured in vercel.json" -ForegroundColor Red
        $allChecks = $false
    }
    
    if ($vercelConfig -match "wsgi") {
        Write-Host "[PASS] WSGI configuration found" -ForegroundColor Green
    } else {
        Write-Host "[WARN] WSGI not configured in vercel.json" -ForegroundColor Red
        $allChecks = $false
    }
}

# Summary
Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

if ($allChecks) {
    Write-Host "`n[SUCCESS] All checks passed!" -ForegroundColor Green
    Write-Host "`nYou're ready to deploy!" -ForegroundColor Green
    Write-Host "`nNext Steps:" -ForegroundColor Yellow
    Write-Host "1. Push code to GitHub:"
    Write-Host "   git init"
    Write-Host "   git add ."
    Write-Host "   git commit -m 'Ready for deployment'"
    Write-Host "   git remote add origin YOUR_GITHUB_REPO_URL"
    Write-Host "   git push -u origin main"
    Write-Host "`n2. Create database at https://neon.tech or https://elephantsql.com"
    Write-Host "`n3. Deploy on Vercel:"
    Write-Host "   - Go to https://vercel.com"
    Write-Host "   - Import your GitHub repository"
    Write-Host "   - Add environment variables (see VERCEL_DEPLOYMENT.md)"
    Write-Host "   - Deploy!"
    Write-Host "`nSee VERCEL_QUICK_START.md for detailed instructions`n" -ForegroundColor Cyan
} else {
    Write-Host "`n[WARNING] Some checks failed!" -ForegroundColor Red
    Write-Host "Please fix the issues above before deploying.`n" -ForegroundColor Red
}

Write-Host "======================================`n" -ForegroundColor Cyan
