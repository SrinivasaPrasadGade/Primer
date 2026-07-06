# Runs NoteAuthNet (4.1) then VoiceSpoofDetector (4.2) back-to-back, stopping
# immediately if a step fails so you don't waste time training the second
# model on top of a broken first one. Each script's own --patience default
# (10 for NoteAuthNet, 7 for VoiceSpoofDetector) is left untouched.
#
# Run from ml\:
#   cd ml
#   .\train_all.ps1

$ErrorActionPreference = "Stop"

function Invoke-Step($command, $description) {
    Write-Host "`n=== $description ===" -ForegroundColor Cyan
    Invoke-Expression $command
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nFAILED: $description (exit code $LASTEXITCODE). Stopping." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

$root = $PSScriptRoot

Set-Location "$root\note-auth-net"
Invoke-Step "python build_manifest.py" "NoteAuthNet: build manifest"
Invoke-Step "python train.py" "NoteAuthNet: train (4.1)"

Set-Location "$root\voice-spoof-detector"
Invoke-Step "python build_manifest.py" "VoiceSpoofDetector: build manifest"
Invoke-Step "python train.py --cache-mels" "VoiceSpoofDetector: train (4.2)"

Set-Location $root
Write-Host "`nBoth models trained. Outputs copied to backend/app/ml/models/." -ForegroundColor Green
Write-Host "Next: verify + commit (see ml/TRAINING.md section 5)."
