$ErrorActionPreference = "Stop"

param(
    [string]$AddonPath = "$env:APPDATA\nvda\addons\vocalizer_automotive_driver",
    [string]$AddonsPath = "$env:APPDATA\nvda\addons"
)

$componentsPath = Join-Path $AddonPath "synthDrivers\vocalizerAutomotive\common\speech\components"
$requiredFiles = @(
    "lid.dat",
    "vautov5.dll",
    "nuan_platform.dll",
    "nuan_platform.dllz",
    "synth_med_fxd_bet2f22.dat"
)

Write-Output "Automotive add-on: $AddonPath"
if (-not (Test-Path -LiteralPath $AddonPath)) {
    Write-Output "ADDON_MISSING"
    exit 1
}

$missing = @()
foreach ($file in $requiredFiles) {
    $path = Join-Path $componentsPath $file
    if (Test-Path -LiteralPath $path) {
        $item = Get-Item -LiteralPath $path
        Write-Output ("RUNTIME_OK {0} bytes={1}" -f $file, $item.Length)
    } else {
        $missing += $file
        Write-Output "RUNTIME_MISSING $file"
    }
}

$voices = @(
    Get-ChildItem -LiteralPath $AddonsPath -Directory -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "vocalizer-voice*" }
)
if ($voices.Count -eq 0) {
    Write-Output "VOICES_MISSING"
} else {
    foreach ($voice in $voices) {
        Write-Output "VOICE_FOUND $($voice.Name)"
    }
}

$licensePath = Join-Path $env:APPDATA "nvda\vocalizer_license.ini"
if (Test-Path -LiteralPath $licensePath) {
    Write-Output "LICENSE_FILE_FOUND $licensePath"
} else {
    Write-Output "LICENSE_FILE_MISSING $licensePath"
}

if ($missing.Count -ne 0) {
    exit 2
}

Write-Output "CHECK_PASS"
