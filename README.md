# Vocalizer Automotive 32-bit Bridge for NVDA

[Polski](README.pl.md) | [Slovenčina](README.sk.md) | English

This project adapts the legacy 32-bit Nuance Vocalizer Automotive 5.5 NVDA
driver for both 32-bit and 64-bit NVDA.

On 32-bit NVDA, the original Automotive driver is loaded directly. On
64-bit NVDA, the bridge runs it in NVDA's dedicated 32-bit synthesizer host.
The method used to route speech audio depends on the installed variant:
standard or brokered audio.

## Important

The package does **not** include separate Vocalizer voice add-ons or the
user-specific `vocalizer_license.ini` file. A valid license is still required
by the runtime and must be imported separately.

This fork is maintained independently. Report issues through this repository and do not direct support requests to vendors or maintainers of the original components. The original Vocalizer Automotive 5.5 project is no longer officially developed or supported. The original add-on author is not responsible for this independent fork, any modifications made to it, or technical support.

## Recommended downloads

### Vocalizer Automotive 2.1.7 — Classic bridge

[Download Vocalizer Automotive 2.1.7](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.1.7/vocalizer_automotive_driver-2.1.7.nvda-addon)

This is the recommended variant for normal daily use. On 64-bit NVDA it uses
the classic compatibility bridge and supports NVDA 2026.1 and newer. On
32-bit NVDA it uses the native direct Automotive driver.

### Vocalizer Automotive 2.2.0-2026-08-03 — Brokered audio

[Download the experimental brokered-audio variant](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.2.0-2026-08-03/vocalizer_automotive_driver-2.2.0-2026-08-03.nvda-addon)

This experimental variant is intended for 64-bit NVDA 2026.2 and newer. It
routes audio from the 32-bit host through the main NVDA audio process, which
enables features such as native NVDA audio ducking and Sonic Pitch
compatibility on the supported path. It has known speech cancellation and
queueing issues, so version 2.1.7 remains recommended for regular use.

### Vocalizer Automotive 2.1.6 — NVDA 2025 compatibility fix

[Download the NVDA 2025 compatibility build](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.1.6-nvda2025/vocalizer_automotive_driver-2.1.6-2025fix.nvda-addon)

This is a special compatibility fix for native 32-bit NVDA 2025.x, based on
Vocalizer Automotive 2.1.6. It is **not** the original Vocalizer Automotive
2.1.6 release published by Tiflotecnia and does not contain a 64-bit NVDA
bridge.

Older date-stamped releases remain available for historical and archival
purposes. Most users should choose one of the three downloads above.

## Installation

1. Choose the appropriate variant from **Recommended downloads** and install
   its `.nvda-addon` file. When using the source checkout instead, copy the
   contents of `addon`—not the `addon` directory itself—into the NVDA add-ons
   directory.
2. The package already contains the required Automotive runtime components.
3. Install your own Vocalizer Automotive voice add-ons separately. Their
   directories normally begin with `vocalizer-voice-`.
4. Start NVDA and open:

   `NVDA menu > Vocalizer Automotive > Enter License`

   The license is copied to:

   `%APPDATA%\nvda\vocalizer_license.ini`

5. Restart NVDA and select the driver matching your NVDA architecture:

   - 32-bit NVDA: `vocalizerAutomotive`
   - 64-bit NVDA: `vocalizerAutomotive32`

## Audio Processing

On 64-bit NVDA 2026.2 and newer, the brokered-audio variant routes speech
audio through the main NVDA process. On 32-bit NVDA, Automotive uses its
native direct path. Sonic Pitch remains compatible with the brokered-audio
path.

This variant supports native NVDA audio ducking. Press `Shift+NVDA+D` to cycle
through NVDA's audio ducking modes. NVDA manages and saves the selected mode
on the brokered 64-bit path. The standard variant does not use this path.

## Available Variants

- **Classic bridge — 2.1.7:** the recommended general-purpose version. It
  loads the 32-bit driver through NVDA's classic compatibility bridge on
  64-bit NVDA 2026.1 and newer, and directly on 32-bit NVDA.
- **Brokered audio — 2.2.0-2026-08-03:** an experimental version for 64-bit
  NVDA 2026.2 and newer. It sends speech audio from the 32-bit host through
  the main NVDA audio process. On 32-bit NVDA it uses the native direct path.
- **Legacy NVDA 2025 compatibility fix — 2.1.6-nvda2025:** a native 32-bit
  build for NVDA 2025.x. It contains no bridge for 64-bit NVDA and is not the
  original Tiflotecnia 2.1.6 release.

Install only one variant at a time.

## Automatic Language Switching

The menu contains **Automatic Language Switching Settings**. The dialog
detects installed Automotive voice resources from their `.hdr` metadata and
stores the selected voice mapping in:

`%APPDATA%\nvda\vocalizer.ini`

The add-on interface includes the original translations for these locales:
`an`, `ar`, `da`, `de`, `el`, `es`, `fi`, `fr`, `gl`, `hr`, `hu`, `it`, `ja`,
`ko`, `nb_NO`, `ne`, `nl`, `pl`, `pt_BR`, `pt_PT`, `ru`, `sk`, `sl`, `tr` and
`zh_CN`. HTML documentation is available in English, Polish and Slovak.
NVDA uses the language selected in its general settings.

The reusable translation template is available at
`addon/locale/vocalizer_automotive_driver.pot`.

## Runtime Check

Run:

```powershell
.\tools\Check-VocalizerAutomotiveRuntime.ps1
```

The script reports required runtime files, detected voice add-ons and the
separate license file. It does not download or include a license.

## Building

To build the complete add-on package:

```powershell
.\tools\Build-PublicAddon.ps1
```

The package is written to `dist` and includes the runtime files stored in the
repository. The build always excludes `vocalizer_license.ini`.

## License

The NVDA driver and bridge source is distributed under GPL-2.0 as described
in [gpl.txt](addon/gpl.txt). The included runtime components
are separate runtime files included with this fork. Voice add-ons and
user-specific license files are not included.
