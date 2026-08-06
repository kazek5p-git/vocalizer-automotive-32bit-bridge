# Changelog

All notable changes to this project are documented in this file.

## [2.2.0] - 2026-08-03

### Changed

* Restored the original Vocalizer Automotive menu wording, descriptions, license file chooser and About information where compatible with 64-bit NVDA and the 32-bit host.
* Added a confirmation before importing a license, explaining that the Automotive engine validates it after restart and that detailed rejection information is not available through the current 64/32-bit bridge.
* Restored the original translated license-removal confirmation and expanded the translation catalog without changing the existing automatic language-switching behavior.
* Restored the original post-import restart prompt, allowing NVDA to restart immediately after a license file is copied successfully.
* Changed the behavior of the **Download More Voices** menu item. It now opens the original download redirection used by the legacy Vocalizer Automotive add-on.
* Improved driver version detection by reading the installed manifest when the add-on API is unavailable, with `unknown` as the final fallback instead of a historical hard-coded version.
* Updated the public package builder to include only the active `nuan_platform.dll`, excluding backup files with suffixed names.
* Updated the add-on manifest for the brokered-audio release.

### Fixed

* Fixed the brokered 32-bit bridge lifecycle when changing the audio output device, preventing the NVDA Settings dialog from becoming unavailable after repeated changes.
* Fixed cleanup of the RPyC pipe streams used by brokered audio, eliminating repeated `Bad file descriptor` errors.
* Fixed audio output device selection on NVDA 2025.1 and later by reading `audio.outputDevice`, with a fallback to the legacy `speech.outputDevice` setting.
* Hardened cleanup after partial 32-bit host initialization failures, avoiding invalid process-handle polling.
* Restored base-language voice groups while retaining the available regional language choices.
* Fixed automatic language switching for regional codes such as `en_US` by falling back to the configured base-language voice when no exact regional voice is configured.

## [2.1.7] - 2026-08-03

### Changed

* Restored the original Vocalizer Automotive menu wording, descriptions, license file chooser and About information where compatible with 64-bit NVDA and the 32-bit host.
* Added a confirmation before importing a license, explaining that the Automotive engine validates it after restart and that detailed rejection information is not available through the current 64/32-bit bridge.
* Restored the original translated license-removal confirmation and expanded the translation catalog without changing the existing automatic language-switching behavior.
* Restored the original post-import restart prompt, allowing NVDA to restart immediately after a license file is copied successfully.
* Changed the behavior of the **Download More Voices** menu item. It now opens the original download redirection used by the legacy Vocalizer Automotive add-on.
* Improved driver version detection by reading the installed manifest when the add-on API is unavailable, with `unknown` as the final fallback instead of a historical hard-coded version.
* Updated the public package builder to include only the active `nuan_platform.dll`, excluding backup files with suffixed names.
* Updated the add-on manifest for the classic bridge release.

### Fixed

* Fixed audio output device selection on NVDA 2025.1 and later by reading `audio.outputDevice`, with a fallback to the legacy `speech.outputDevice` setting.
* Restored base-language voice groups while retaining the available regional language choices.
* Fixed automatic language switching for regional codes such as `en_US` by falling back to the configured base-language voice when no exact regional voice is configured.
