# Workmate — Stop All Services
# Run: powershell -File stop.ps1

Write-Host ""
Write-Host " Stopping Workmate services..." -ForegroundColor Yellow

# Kill uvicorn (FastAPI backend)
$uvicorn = Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue
if ($uvicorn) {
    Stop-Process -Name "uvicorn" -Force
    Write-Host " ✅  Backend (uvicorn) stopped." -ForegroundColor Green
} else {
    Write-Host " ℹ️   Backend not running." -ForegroundColor Gray
}

# Kill python http.server on port 3000
$frontend = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($frontend) {
    Stop-Process -Id $frontend -Force -ErrorAction SilentlyContinue
    Write-Host " ✅  Frontend (HTTP server) stopped." -ForegroundColor Green
} else {
    Write-Host " ℹ️   Frontend not running." -ForegroundColor Gray
}

Write-Host ""
Write-Host " All services stopped." -ForegroundColor Cyan
