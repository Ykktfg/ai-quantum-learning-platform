$ErrorActionPreference = "Continue"

$base = "http://127.0.0.1:8000"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AI QUANTUM LEARNING PLATFORM" -ForegroundColor Cyan
Write-Host " BACKEND INTEGRATION CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET"
    )

    try {
        if ($Method -eq "GET") {
            $response = Invoke-RestMethod -Uri $Url -Method Get
        }

        Write-Host "[PASS] $Name" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[FAIL] $Name" -ForegroundColor Red
        Write-Host "       $($_.Exception.Message)" -ForegroundColor DarkRed
        return $false
    }
}

$passed = 0
$failed = 0

# ----------------------------------------
# 1. Backend Health
# ----------------------------------------

if (Test-Endpoint "Backend Health" "$base/api/health") {
    $passed++
} else {
    $failed++
}

# ----------------------------------------
# 2. Root
# ----------------------------------------

if (Test-Endpoint "Backend Root" "$base/") {
    $passed++
} else {
    $failed++
}

# ----------------------------------------
# 3. OpenAPI
# ----------------------------------------

try {
    $openapi = Invoke-RestMethod "$base/openapi.json"

    Write-Host "[PASS] OpenAPI" -ForegroundColor Green
    $passed++

    Write-Host ""
    Write-Host "Registered API Routes:" -ForegroundColor Yellow

    $openapi.paths.PSObject.Properties.Name |
        Sort-Object |
        ForEach-Object {
            Write-Host "  $_"
        }
}
catch {
    Write-Host "[FAIL] OpenAPI" -ForegroundColor Red
    $failed++
}

# ----------------------------------------
# 4. Important Backend Routes
# ----------------------------------------

$routes = @(
    "/api/users/me",
    "/api/courses",
    "/api/enrollments/me",
    "/api/progress/me",
    "/api/progress/analytics",
    "/api/activity/me",
    "/api/analytics",
    "/api/analytics/profile",
    "/api/analytics/skills",
    "/api/analytics/achievements",
    "/api/analytics/activity",
    "/api/analytics/weak-topics",
    "/api/analytics/recommendations",
    "/api/me/dashboard",
    "/api/circuits",
    "/api/simulations/me"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " ROUTE AVAILABILITY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

foreach ($route in $routes) {

    try {
        $null = Invoke-RestMethod "$base$route" -Method Get

        Write-Host "[PASS] $route" -ForegroundColor Green
        $passed++
    }
    catch {

        $status = $_.Exception.Response.StatusCode.value__

        # 401 means the route exists but requires authentication.
        if ($status -eq 401) {
            Write-Host "[PASS] $route  (Authentication required)" -ForegroundColor Green
            $passed++
        }
        elseif ($status -eq 405) {
            Write-Host "[PASS] $route  (Method exists, GET not allowed)" -ForegroundColor Green
            $passed++
        }
        else {
            Write-Host "[FAIL] $route  HTTP $status" -ForegroundColor Red
            $failed++
        }
    }
}

# ----------------------------------------
# 5. Quantum Service
# ----------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " QUANTUM SERVICE :8001" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

try {
    $quantumHealth = Invoke-RestMethod "http://127.0.0.1:8001/health" -TimeoutSec 5

    Write-Host "[PASS] Quantum Health" -ForegroundColor Green
    $quantumHealth | Format-List

    $passed++
}
catch {
    Write-Host "[FAIL] Quantum Health" -ForegroundColor Red
    Write-Host "       Quantum service is not reachable on port 8001."
    $failed++
}

# ----------------------------------------
# 6. AI Service
# ----------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AI SERVICE :8002" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

try {
    $aiHealth = Invoke-RestMethod "http://127.0.0.1:8002/health" -TimeoutSec 5

    Write-Host "[PASS] AI Health" -ForegroundColor Green
    $aiHealth | Format-List

    $passed++
}
catch {
    Write-Host "[FAIL] AI Health" -ForegroundColor Red
    Write-Host "       AI service is not reachable on port 8002."
    $failed++
}

# ----------------------------------------
# 7. Backend Tests
# ----------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " PYTEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

python -m pytest -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "[PASS] Backend Test Suite" -ForegroundColor Green
    $passed++
}
else {
    Write-Host "[FAIL] Backend Test Suite" -ForegroundColor Red
    $failed++
}

# ----------------------------------------
# Summary
# ----------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " FINAL SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Checks Passed : $passed" -ForegroundColor Green
Write-Host "Checks Failed : $failed" -ForegroundColor Red

if ($failed -eq 0) {
    Write-Host ""
    Write-Host "ALL CHECKS PASSED" -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host "SOME CHECKS NEED ATTENTION" -ForegroundColor Yellow
}

Write-Host ""