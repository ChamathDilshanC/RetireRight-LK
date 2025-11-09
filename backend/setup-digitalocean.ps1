# Quick Setup Script for DigitalOcean Deployment
# Generates all necessary configuration values

Write-Host ""
Write-Host "🚀 DigitalOcean Deployment Configuration Generator" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Generate SECRET_KEY
Write-Host "1️⃣  Generating SECRET_KEY..." -ForegroundColor Yellow
$secretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})
Write-Host "   ✅ SECRET_KEY generated" -ForegroundColor Green
Write-Host ""

# 2. Check for Firebase file
Write-Host "2️⃣  Checking Firebase service account..." -ForegroundColor Yellow
$jsonFile = "firebase-service-account.json"
$firebaseBase64 = ""

if (Test-Path $jsonFile) {
    Write-Host "   ✅ Found $jsonFile" -ForegroundColor Green
    $content = Get-Content $jsonFile -Raw
    $firebaseBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))
    Write-Host "   ✅ Converted to base64" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  firebase-service-account.json not found" -ForegroundColor Red
    Write-Host "   You'll need to download this from Firebase Console" -ForegroundColor Yellow
}
Write-Host ""

# 3. Display all values
Write-Host "🎯 COPY THESE VALUES TO DIGITALOCEAN" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "App Platform -> Settings -> Environment Variables" -ForegroundColor White
Write-Host ""

Write-Host "Variable 1:" -ForegroundColor Yellow
Write-Host "  Key:   FLASK_ENV" -ForegroundColor White
Write-Host "  Value: production" -ForegroundColor Green
Write-Host ""

Write-Host "Variable 2:" -ForegroundColor Yellow
Write-Host "  Key:   SECRET_KEY" -ForegroundColor White
Write-Host "  Value: $secretKey" -ForegroundColor Green
Write-Host ""

Write-Host "Variable 3:" -ForegroundColor Yellow
Write-Host "  Key:   FRONTEND_URL" -ForegroundColor White
Write-Host "  Value: https://your-frontend-app.ondigitalocean.app" -ForegroundColor Cyan
Write-Host "         WARNING: Replace with your actual frontend URL!" -ForegroundColor Red
Write-Host ""

Write-Host "Variable 4:" -ForegroundColor Yellow
Write-Host "  Key:   FIREBASE_PROJECT_ID" -ForegroundColor White
Write-Host "  Value: retireright-lk-41def" -ForegroundColor Green
Write-Host ""

if ($firebaseBase64) {
    Write-Host "Variable 5:" -ForegroundColor Yellow
    Write-Host "  Key:   FIREBASE_SERVICE_ACCOUNT_BASE64" -ForegroundColor White
    Write-Host "  Value: <Copied to clipboard - press Ctrl+V>" -ForegroundColor Green
    $firebaseBase64 | Set-Clipboard
    Write-Host "         SUCCESS: Base64 is in your clipboard!" -ForegroundColor Green
} else {
    Write-Host "Variable 5:" -ForegroundColor Yellow
    Write-Host "  Key:   FIREBASE_SERVICE_ACCOUNT_BASE64" -ForegroundColor White
    Write-Host "  Value: <Download from Firebase Console first>" -ForegroundColor Red
}
Write-Host ""

Write-Host "RUN COMMAND" -ForegroundColor Cyan
Write-Host "==============" -ForegroundColor Cyan
Write-Host "App Platform -> Backend Service -> Settings -> Run Command" -ForegroundColor White
Write-Host ""
Write-Host "gunicorn run:app --bind 0.0.0.0:`$PORT" -ForegroundColor Green
Write-Host ""

Write-Host "SUCCESS DONE!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to DigitalOcean App Platform" -ForegroundColor White
Write-Host "2. Set the 5 environment variables above" -ForegroundColor White
Write-Host "3. Set the run command" -ForegroundColor White
Write-Host "4. Push code to GitHub" -ForegroundColor White
Write-Host "5. Redeploy the app" -ForegroundColor White
Write-Host ""

# Save to file for reference
$outputFile = "digitalocean-config.txt"
@"
DigitalOcean Configuration
==========================
Generated: $(Get-Date)

ENVIRONMENT VARIABLES:
---------------------
FLASK_ENV=production
SECRET_KEY=$secretKey
FRONTEND_URL=https://your-frontend-app.ondigitalocean.app
FIREBASE_PROJECT_ID=retireright-lk-41def
FIREBASE_SERVICE_ACCOUNT_BASE64=<in-clipboard>

RUN COMMAND:
-----------
gunicorn run:app --bind 0.0.0.0:`$PORT

SOURCE DIRECTORY:
----------------
backend

HEALTH CHECK:
------------
Path: /health
Port: 8080
"@ | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "📄 Configuration saved to: $outputFile" -ForegroundColor Cyan
Write-Host ""
