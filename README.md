# Vocalizer Automotive 32-bit Bridge for NVDA

[Polski](README.pl.md) | [Slovenčina](README.sk.md) | English

This project adapts the legacy 32-bit Nuance Vocalizer Automotive 5.5 NVDA
driver for both 32-bit and 64-bit NVDA.

On 32-bit NVDA, the original Automotive driver is loaded directly. On 64-bit
NVDA, the bridge runs it in NVDA's dedicated 32-bit synthesizer host.

On 64-bit NVDA 2026.2 and newer, this branch uses NVDA's brokered-audio path.
For the classic 64-bit bridge, use release `v2.1.7`.

## Important

The package includes the bridge code and the Vocalizer runtime components
required by the 32-bit Automotive host:

- `vautov5.dll`
- `nuan_platform.dll`
- `nuan_platform.dllz`
- the required component data and tuning files

The package does **not** include separate Vocalizer voice add-ons or the
user-specific `vocalizer_license.ini` file. A valid license is still required
by the runtime and must be imported separately.

This fork is maintained independently. Report issues through this repository
and do not direct support requests to vendors or maintainers of the original
components. The original Vocalizer Automotive 5.5 project is abandonware, and
its original add-on author is not responsible for this fork or its support.

## Installation

1. Install the public `.nvda-addon` file from the GitHub Releases page, or
   copy this repository into the NVDA add-ons directory.
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

On 64-bit NVDA 2026.2 and newer, this release uses NVDA's brokered-audio
service to route speech audio through the main NVDA process. On 32-bit NVDA,
the original Automotive driver uses its direct native path. Sonic Pitch
remains compatible with the brokered audio path.

Native NVDA audio ducking is available in this variant. Press
`Shift+NVDA+D` to cycle through NVDA's audio ducking modes. The selected mode
is managed and saved by NVDA on the brokered 64-bit path. The classic
`v2.1.7` variant does not use this brokered-audio path.

## Release Variants

- `v2.1.7`: classic bridge for 32-bit NVDA and 64-bit NVDA 2026.1 and newer.
- `v2.2.0`: brokered-audio bridge for 64-bit NVDA 2026.2 and newer, with a
  direct 32-bit NVDA path.

Install only one variant of the add-on at a time.

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
`locale/vocalizer_automotive_driver.pot`.

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
in [LICENSE](LICENSE) and [gpl.txt](gpl.txt). The included runtime components
are separate runtime files included with this fork. Voice add-ons and
user-specific license files are not included.
