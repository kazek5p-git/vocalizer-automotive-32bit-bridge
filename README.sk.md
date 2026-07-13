# 32-bitový most Vocalizer Automotive pre NVDA

[English](README.md) | [Polski](README.pl.md) | Slovenčina

Projekt upravuje starší 32-bitový ovládač Nuance Vocalizer Automotive 5.5
tak, aby fungoval v 64-bitových verziách NVDA od 2026.2 a novších.

Most spúšťa pôvodný 32-bitový ovládač vo vyhradenom hostiteľovi syntetizátora
NVDA pomocou štandardného mosta kompatibility NVDA.

Táto vetva obsahuje variant brokered audio a vyžaduje NVDA 2026.2 alebo
novší. Pre NVDA 2026.1 použite vetvu `main` a vydanie `v2.1.7`.

## Dôležité

Toto úložisko zámerne neobsahuje:

- `vautov5.dll`
- `nuan_platform.dll`
- hlasové údaje Vocalizer
- licenčné súbory Vocalizer

Ide o vlastnícke súbory alebo súbory chránené licenciou. Použite vlastnú
legálne získanú kópiu. Nenahrávajte ich do tohto úložiska.

Projekt nie je prepojený s NV Access, Tiflotecnia, Nuance ani Cerence.

## Inštalácia

1. Nainštalujte verejný súbor `.nvda-addon` zo stránky GitHub Releases alebo
   skopírujte toto úložisko do priečinka doplnkov NVDA.
2. Vložte vlastné runtime knižnice do priečinka:

   `%APPDATA%\nvda\addons\vocalizer_automotive_driver\synthDrivers\vocalizerAutomotive\common\speech\components`

   Požadované súbory:

   - `vautov5.dll`
   - `nuan_platform.dll`

3. Samostatne nainštalujte vlastné doplnky s hlasmi Vocalizer Automotive.
   Ich priečinky sa zvyčajne začínajú na `vocalizer-voice-`.
4. Spustite NVDA a otvorte:

   `Ponuka NVDA > Vocalizer Automotive > Zadať licenciu`

   Licencia sa skopíruje do:

   `%APPDATA%\nvda\vocalizer_license.ini`

5. Reštartujte NVDA a vyberte syntetizátor:

   `vocalizerAutomotive32`

## Spracovanie zvuku

Toto vydanie používa službu brokered audio NVDA na odovzdanie zvuku reči cez
hlavný proces NVDA. Vyžaduje NVDA 2026.2 alebo novší. Sonic Pitch zostáva
kompatibilný s touto audio cestou.

## Varianty vydaní

- `v2.1.7`: klasický most pre NVDA 2026.1 a novšie.
- `v2.2.0`: most brokered audio pre NVDA 2026.2 a novšie.

Inštalujte naraz iba jeden variant doplnku. Variant brokered odovzdáva zvuk
reči cez hlavnú audio službu NVDA; klasický variant je správnou voľbou pre
NVDA 2026.1.

## Automatické prepínanie jazyka

V ponuke sa nachádza položka **Nastavenia automatického prepínania jazyka**.
Dialóg vyhľadá nainštalované hlasy Automotive podľa metadát `.hdr` a uloží
vybrané priradenia hlasov do:

`%APPDATA%\nvda\vocalizer.ini`

## Kontrola prostredia

Spustite:

```powershell
.\tools\Check-VocalizerAutomotiveRuntime.ps1
```

Skript zobrazí chýbajúce runtime knižnice a nájdené hlasové doplnky. Nesťahuje
ani nepridáva vlastnícke súbory.

## Zostavenie

Ak chcete vytvoriť verejný doplnok bez runtime súborov:

```powershell
.\tools\Build-PublicAddon.ps1
```

Balík sa uloží do priečinka `dist`.

Univerzálna šablóna prekladov sa nachádza v súbore
`locale/vocalizer_automotive_driver.pot`.

## Licencia

Zdrojový kód ovládača NVDA a mosta je distribuovaný pod licenciou GPL-2.0
podľa súborov [LICENSE](LICENSE) a [gpl.txt](gpl.txt). Táto licencia
neudeľuje právo na redistribúciu externých binárnych súborov Vocalizer,
hlasových údajov ani licenčných súborov.
