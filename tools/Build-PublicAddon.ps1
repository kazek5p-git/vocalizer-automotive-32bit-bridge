param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) "dist")
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repositoryRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path.TrimEnd("\")
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$manifestPath = Join-Path $repositoryRoot "manifest.ini"
$manifestText = Get-Content -LiteralPath $manifestPath -Raw
$versionMatch = [regex]::Match($manifestText, '(?m)^version\s*=\s*(.+)$')
if (-not $versionMatch.Success) {
    throw "Could not read add-on version from manifest.ini."
}
$version = $versionMatch.Groups[1].Value.Trim().Trim('"')
$target = Join-Path $OutputDirectory "VocalizerAutomotiveDriver-V.$version.nvda-addon"

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Force
}

$archive = [System.IO.Compression.ZipFile]::Open(
    $target,
    [System.IO.Compression.ZipArchiveMode]::Create
)
try {
    Get-ChildItem -LiteralPath $repositoryRoot -Recurse -File -Force | ForEach-Object {
        $relative = $_.FullName.Substring($repositoryRoot.Length + 1)
        $parts = $relative -split "\\"
        if ($parts | Where-Object { $_ -in @(".git", "dist", "tools", "tests", "__pycache__") }) {
            return
        }
        if ($_.Extension -in @(".pyc", ".pyo")) {
            return
        }
        if ($_.Name -eq "vocalizer_license.ini") {
            return
        }
        if ($_.Extension -in @(".md", ".ps1", ".gitignore", ".pot")) {
            return
        }
        $entry = $archive.CreateEntry(
            ($relative -replace "\\", "/"),
            [System.IO.Compression.CompressionLevel]::Optimal
        )
        $input = [System.IO.File]::OpenRead($_.FullName)
        try {
            $output = $entry.Open()
            try {
                $input.CopyTo($output)
            } finally {
                $output.Dispose()
            }
        } finally {
            $input.Dispose()
        }
    }
} finally {
    $archive.Dispose()
}

$package = [System.IO.Compression.ZipFile]::OpenRead($target)
try {
    $names = @($package.Entries | ForEach-Object { $_.FullName })
    $forbidden = @(
        $names | Where-Object {
            $_ -match "(^|/)(.*\.py[co]$|vocalizer_license\.ini$)"
        }
    )
    $requiredRuntime = @(
        "synthDrivers/vocalizerAutomotive/common/speech/components/lid.dat",
        "synthDrivers/vocalizerAutomotive/common/speech/components/nuan_platform.dll",
        "synthDrivers/vocalizerAutomotive/common/speech/components/nuan_platform.dllz",
        "synthDrivers/vocalizerAutomotive/common/speech/components/synth_med_fxd_bet2f22.dat",
        "synthDrivers/vocalizerAutomotive/common/speech/components/vautov5.dll"
    )
    $missingRuntime = @($requiredRuntime | Where-Object { $_ -notin $names })
    if (
        $forbidden.Count -ne 0 -or
        $missingRuntime.Count -ne 0 -or
        "manifest.ini" -notin $names
    ) {
        throw "Full package validation failed. Forbidden=$($forbidden -join ', ') MissingRuntime=$($missingRuntime -join ', ')"
    }
    Write-Output ("FULL_PACKAGE_OK {0} entries={1} bytes={2}" -f $target, $names.Count, (Get-Item -LiteralPath $target).Length)
} finally {
    $package.Dispose()
}
