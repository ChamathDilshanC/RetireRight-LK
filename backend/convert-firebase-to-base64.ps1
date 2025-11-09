# Firebase Service Account to Base64 Converter
# Run this script to convert firebase-service-account.json to base64 for DigitalOcean

$jsonFile = "firebase-service-account.json"

if (Test-Path $jsonFile) {
    Write-Host "✅ Found $jsonFile" -ForegroundColor Green

    # Read file content
    $content = Get-Content $jsonFile -Raw

    # Convert to base64
    $base64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))

    # Copy to clipboard
    $base64 | Set-Clipboard

    Write-Host ""
    Write-Host "✅ Base64 encoded and copied to clipboard!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Go to DigitalOcean App Platform" -ForegroundColor White
    Write-Host "2. Navigate to: App → Settings → Environment Variables" -ForegroundColor White
    Write-Host "3. Add new variable:" -ForegroundColor White
    Write-Host "   Key: FIREBASE_SERVICE_ACCOUNT_BASE64" -ForegroundColor Cyan
    Write-Host "   Value: <Paste from clipboard (Ctrl+V)>" -ForegroundColor Cyan
    Write-Host "4. Save and redeploy" -ForegroundColor White
    Write-Host ""
    Write-Host "The base64 string is also shown below:" -ForegroundColor Yellow
    Write-Host $base64 -ForegroundColor DarkGray

} else {
    Write-Host "❌ Error: $jsonFile not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure firebase-service-account.json exists in the backend folder." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To get this file:" -ForegroundColor Yellow
    Write-Host "1. Go to https://console.firebase.google.com/" -ForegroundColor White
    Write-Host "2. Select your project" -ForegroundColor White
    Write-Host "3. Click ⚙️ → Project Settings" -ForegroundColor White
    Write-Host "4. Service accounts tab" -ForegroundColor White
    Write-Host "5. Generate new private key" -ForegroundColor White
    Write-Host "6. Save as firebase-service-account.json in this folder" -ForegroundColor White
}
