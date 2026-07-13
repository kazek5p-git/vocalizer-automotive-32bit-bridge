param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) "dist")
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repositoryRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path.TrimEnd("\")
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$date = Get-Date -Format "yyyyMMdd"
$target = Join-Path $OutputDirectory "VocalizerAutomotiveDriver-public-$date.nvda-addon"

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
        if ($_.Extension -in @(".dll", ".dllz", ".dat", ".dcb", ".rules", ".hdr", ".pyc", ".pyo")) {
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
            $_ -match "(^|/)(.*\.dll|.*\.dllz|.*\.dat|.*\.dcb|.*\.rules|.*\.hdr|.*\.py[co]$|vocalizer_license\.ini$)"
        }
    )
    if ($forbidden.Count -ne 0 -or "manifest.ini" -notin $names) {
        throw "Public package contains forbidden files."
    }
    Write-Output ("PUBLIC_PACKAGE_OK {0} entries={1} bytes={2}" -f $target, $names.Count, (Get-Item -LiteralPath $target).Length)
} finally {
    $package.Dispose()
}
