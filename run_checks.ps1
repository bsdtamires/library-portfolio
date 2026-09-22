<#
.SYNOPSIS
    Runs every .sql file in checks/ against db/library.db using the sqlite3
    CLI directly — no Python involved in running the checks themselves.

.DESCRIPTION
    Convention (the same one dbt uses, without needing dbt): each .sql file
    is a SELECT query. Zero rows returned = PASS. Any row returned = FAIL,
    and the returned rows ARE the offending data.

    Requires the sqlite3 command-line tool to be installed and on PATH.

.EXAMPLE
    .\run_checks.ps1
#>

$DbPath = "db/library.db"
$ChecksDir = "checks"

if (-not (Test-Path $DbPath)) {
    Write-Host "Database not found at $DbPath — run 'python src/seed_data.py' first."
    exit 1
}

$passCount = 0
$failCount = 0

Get-ChildItem -Path $ChecksDir -Filter "*.sql" | Sort-Object Name | ForEach-Object {
    $checkFile = $_.FullName
    $name = $_.Name

    $result = Get-Content $checkFile -Raw | sqlite3 $DbPath

    if ([string]::IsNullOrWhiteSpace($result)) {
        Write-Host "PASS  $name"
        $script:passCount++
    } else {
        Write-Host "FAIL  $name"
        $result -split "`n" | ForEach-Object { Write-Host "      $_" }
        $script:failCount++
    }
}

Write-Host ""
Write-Host "$passCount passed, $failCount failed"

if ($failCount -gt 0) {
    exit 1
}
exit 0
