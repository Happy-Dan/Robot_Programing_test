$ErrorActionPreference = "Continue"

function Test-Command($Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $cmd) {
        Write-Host "[NG] $Name is not available in PATH" -ForegroundColor Red
        return $false
    }
    Write-Host "[OK] $Name => $($cmd.Source)" -ForegroundColor Green
    return $true
}

Write-Host "Offline Code AI environment check"
Write-Host ""

$hasPython = Test-Command "python"
$hasOllama = Test-Command "ollama"

Write-Host ""
if ($hasPython) {
    python --version
}

if ($hasOllama) {
    ollama --version
    Write-Host ""
    Write-Host "Installed models:"
    ollama list
}

Write-Host ""
Write-Host "Next steps:"
if (-not $hasPython) {
    Write-Host "- Install Python 3.10+ and enable 'Add python.exe to PATH'."
}
if (-not $hasOllama) {
    Write-Host "- Install Ollama, then run: ollama pull qwen2.5-coder:7b"
}
if ($hasPython -and $hasOllama) {
    Write-Host "- Start Ollama with: ollama serve"
    Write-Host "- Then test with: python .\offline_code_ai.py --ask `"PythonでHello Worldを書いて`""
}
