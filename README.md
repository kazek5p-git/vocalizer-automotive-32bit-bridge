# Vocalizer Automotive 2.1.6 – NVDA 2025 compatibility branch

This branch preserves the original native 32-bit Vocalizer Automotive 5.5
driver released by Tiflotecnia as version 2.1.6, with a small compatibility
fix for NVDA 2025.x.

It is intentionally separate from the 32-bit bridge development in the
`main` and `brokered-audio` branches.

## Purpose

Vocalizer Automotive is a native 32-bit synthesizer. This branch is intended
for users who still run a 32-bit version of NVDA and want to retain the
original driver behavior without using the compatibility bridge required by
64-bit NVDA.

This includes the original Automotive integration and behavior, including its
native license handling and messages.

## Compatibility

- Native 32-bit NVDA only
- Intended for NVDA 2025.x
- Does not contain the 32-bit bridge for 64-bit NVDA
- For current 64-bit NVDA, use the `main` or `brokered-audio` branch instead

## Changes from Vocalizer Automotive 2.1.6

The synthesis engine and normal Vocalizer driver behavior have not been
redesigned.

The main compatibility fix changes audio output device detection:

- NVDA 2025.1 and later: reads `audio.outputDevice`
- Older NVDA versions: falls back to the legacy `speech.outputDevice`
- If neither configuration value is available, the default audio device is
  used

The package also contains the maintained Polish and Slovak translations and
the intended localization updates included in this archived branch.

The modified `_vocalizer.py` file carries an explicit modification notice
identifying DJ Graco as the author of the 2025 compatibility fix.

## Important

This is not an official Tiflotecnia release. It is a preservation and
compatibility update based on the final Tiflotecnia 2.1.6 driver.

A valid Vocalizer Automotive license and compatible voice add-ons are still
required. User-specific license files and separate voice packages are not
provided by this repository.

The original Vocalizer Automotive project is no longer officially maintained
or supported by Tiflotecnia.

## Other branches

- `main` – Vocalizer Automotive 2.1.7 Classic bridge
- `brokered-audio` – experimental brokered-audio version for modern 64-bit NVDA
- `legacy-2.1.6-2025` – native 32-bit 2.1.6 compatibility version for NVDA 2025.x

## License

The NVDA driver source is distributed under the GNU General Public License
as described in `gpl.txt`.
