# Vocalizer Automotive 32-bit Bridge for NVDA

[Polski](README.pl.md) | [Slovenčina](README.sk.md) | English

This project adapts the legacy 32-bit Nuance Vocalizer Automotive 5.5 NVDA
driver for 64-bit NVDA 2026.2 and newer.

The bridge runs the original 32-bit driver in NVDA's dedicated 32-bit
synthesizer host using NVDA's standard compatibility bridge.

This branch contains the brokered-audio variant and requires NVDA 2026.2 or
newer. For NVDA 2026.1, use the `main` branch and release `v2.1.7`.

## Important

This repository intentionally does **not** contain:

- `vautov5.dll`
- `nuan_platform.dll`
- Vocalizer voice data
- Vocalizer license files

Those files are proprietary or license-controlled. You must obtain and use
your own legally licensed copy. Do not upload them to this repository.

The project is not affiliated with NV Access, Tiflotecnia, Nuance, or Cerence.

## Installation

1. Install the public `.nvda-addon` file from the GitHub Releases page, or
   copy this repository into the NVDA add-ons directory.
2. Place your own runtime DLLs in:

   `%APPDATA%\nvda\addons\vocalizer_automotive_driver\synthDrivers\vocalizerAutomotive\common\speech\components`

   Required files:

   - `vautov5.dll`
   - `nuan_platform.dll`

3. Install your own Vocalizer Automotive voice add-ons separately. Their
   directories normally begin with `vocalizer-voice-`.
4. Start NVDA and open:

   `NVDA menu > Vocalizer Automotive > Enter License`

   The license is copied to:

   `%APPDATA%\nvda\vocalizer_license.ini`

5. Restart NVDA and select:

   `vocalizerAutomotive32`

## Audio Processing

This release uses NVDA's brokered-audio service to route speech audio through
the main NVDA process. This requires NVDA 2026.2 or newer. Sonic Pitch remains
compatible with the brokered audio path.

## Release Variants

- `v2.1.7`: classic bridge for NVDA 2026.1 and newer.
- `v2.2.0`: brokered-audio bridge for NVDA 2026.2 and newer.

Install only one variant of the add-on at a time. The brokered variant routes
speech audio through NVDA's main audio service; the classic variant is the
compatible choice for NVDA 2026.1.

## Automatic Language Switching

The menu contains **Automatic Language Switching Settings**. The dialog
detects installed Automotive voice resources from their `.hdr` metadata and
stores the selected voice mapping in:

`%APPDATA%\nvda\vocalizer.ini`

The add-on interface and documentation are available in English, Polish and
Slovak. NVDA uses the language selected in its general settings.

The reusable translation template is available at
`locale/vocalizer_automotive_driver.pot`.

## Runtime Check

Run:

```powershell
.\tools\Check-VocalizerAutomotiveRuntime.ps1
```

The script reports missing runtime DLLs and detected voice add-ons. It does
not download or include proprietary files.

## Building

To build a public add-on package without runtime files:

```powershell
.\tools\Build-PublicAddon.ps1
```

The package is written to `dist`.

## License

The NVDA driver and bridge source is distributed under GPL-2.0 as described
in [LICENSE](LICENSE) and [gpl.txt](gpl.txt). This license does not grant
rights to redistribute third-party Vocalizer binaries, voice data, or
license files.
