# Vocalizer Automotive 2.1.6 – verzia kompatibility pre NVDA 2025

[English](README.md) | [Polski](README.pl.md) | Slovenčina

Táto vetva zachováva pôvodný natívny 32-bitový ovládač Vocalizer
Automotive 5.5, ktorý Tiflotecnia vydala ako verziu 2.1.6, s malou
opravou kompatibility pre NVDA 2025.x.

Zámerne je oddelená od vývoja 32-bitového mosta vo vetvách `main`
a `brokered-audio`.

## Účel

Vocalizer Automotive je natívny 32-bitový syntetizátor. Táto vetva je
určená používateľom, ktorí stále používajú 32-bitovú verziu NVDA a chcú
zachovať pôvodné správanie ovládača bez použitia mosta kompatibility,
ktorý vyžaduje 64-bitové NVDA.

Tým sa zachováva pôvodná integrácia a správanie Automotive vrátane
natívnej práce s licenciou a licenčných hlásení.

## Kompatibilita

- Iba natívne 32-bitové NVDA
- Určené pre NVDA 2025.x
- Neobsahuje 32-bitový most pre 64-bitové NVDA
- Pre aktuálne 64-bitové verzie NVDA použite vetvu `main` alebo
  `brokered-audio`

## Zmeny oproti Vocalizer Automotive 2.1.6

Syntetizačný engine ani bežné správanie ovládača Vocalizer neboli
prepracované.

Hlavná oprava kompatibility mení zisťovanie výstupného zvukového zariadenia:

- NVDA 2025.1 a novšie: používa sa `audio.outputDevice`
- Staršie verzie NVDA: ako záložná možnosť sa používa pôvodné
  `speech.outputDevice`
- Ak nie je dostupná ani jedna hodnota konfigurácie, použije sa predvolené
  zvukové zariadenie

Balík obsahuje aj udržiavané poľské a slovenské preklady a zamýšľané
aktualizácie lokalizácie zachované v tejto archívnej vetve.

Upravený súbor `_vocalizer.py` obsahuje jasné oznámenie, že autorom opravy
kompatibility pre NVDA 2025 je DJ Graco.

## Dôležité

Toto nie je oficiálne vydanie Tiflotecnie. Ide o zachovanú a kompatibilnú
verziu založenú na poslednom ovládači Tiflotecnie vo verzii 2.1.6.

Naďalej je potrebná platná licencia Vocalizer Automotive a kompatibilné
hlasové doplnky. Používateľské licenčné súbory ani samostatné hlasové
balíky nie sú poskytované v tomto úložisku.

Pôvodný projekt Vocalizer Automotive už Tiflotecnia oficiálne nevyvíja
ani nepodporuje.

## Ostatné vetvy

- `main` – Vocalizer Automotive 2.1.7 Classic bridge
- `brokered-audio` – experimentálna verzia brokered audio pre súčasné
  64-bitové NVDA
- `legacy-2.1.6-2025` – natívna 32-bitová verzia 2.1.6 upravená pre
  NVDA 2025.x

## Licencia

Zdrojový kód ovládača NVDA je distribuovaný pod GNU General Public License
podľa súboru [gpl.txt](addon/gpl.txt).
