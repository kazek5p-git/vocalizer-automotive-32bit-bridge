# 32-bitový most Vocalizer Automotive pre NVDA

[English](README.md) | [Polski](README.pl.md) | Slovenčina

Projekt upravuje starší 32-bitový ovládač Nuance Vocalizer Automotive 5.5
tak, aby fungoval v 64-bitových verziách NVDA od 2026.2 a novších.

Most spúšťa pôvodný 32-bitový ovládač vo vyhradenom hostiteľovi syntetizátora
NVDA pomocou štandardného mosta kompatibility NVDA.

Táto vetva obsahuje variant brokered audio a vyžaduje NVDA 2026.2 alebo
novší. Pre NVDA 2026.1 použite vetvu `main` a vydanie `v2.1.7`.

## Dôležité

Balík obsahuje kód mosta a runtime súbory potrebné 32-bitovým hostiteľom
Automotive:

- `vautov5.dll`
- `nuan_platform.dll`
- `nuan_platform.dllz`
- požadované údaje komponentov a súbory ladenia

Balík neobsahuje samostatné hlasové doplnky Vocalizer ani používateľský súbor
`vocalizer_license.ini`. Runtime stále vyžaduje platnú licenciu, ktorú treba
importovať samostatne.

Tento fork je udržiavaný nezávisle. Problémy hláste v tomto úložisku a žiadosti
o podporu neposielajte dodávateľom ani správcom pôvodných komponentov.
Pôvodný projekt Vocalizer Automotive 5.5 je abandonware a pôvodný autor doplnku
nezodpovedá za tento fork ani za jeho podporu.

## Inštalácia

1. Nainštalujte verejný súbor `.nvda-addon` zo stránky GitHub Releases alebo
   skopírujte toto úložisko do priečinka doplnkov NVDA.
2. Balík už obsahuje požadované runtime súbory Automotive.
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

Tento variant podporuje natívne stlmenie zvuku NVDA. Skratka
`Shift+NVDA+D` prepína režimy stlmenia zvuku dostupné v NVDA. Vybraný režim
spravuje a ukladá samotné NVDA. Klasický variant `v2.1.7` túto cestu brokered
audio nepoužíva.

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

Skript zobrazí požadované runtime súbory, nájdené hlasové doplnky a samostatný
licenčný súbor. Nesťahuje ani nepridáva licenciu.

## Zostavenie

Ak chcete vytvoriť kompletný doplnok:

```powershell
.\tools\Build-PublicAddon.ps1
```

Balík sa uloží do priečinka `dist` a bude obsahovať runtime súbory uložené
v úložisku. Skript vždy vynechá `vocalizer_license.ini`.

Univerzálna šablóna prekladov sa nachádza v súbore
`locale/vocalizer_automotive_driver.pot`.

Rozhranie doplnku obsahuje lokalizácie: `an`, `ar`, `da`, `de`, `el`, `es`,
`fi`, `fr`, `gl`, `hr`, `hu`, `it`, `ja`, `ko`, `nb_NO`, `ne`, `nl`, `pl`,
`pt_BR`, `pt_PT`, `ru`, `sk`, `sl`, `tr` a `zh_CN`. HTML dokumentácia je
dostupná v angličtine, poľštine a slovenčine.

## Licencia

Zdrojový kód ovládača NVDA a mosta je distribuovaný pod licenciou GPL-2.0
podľa súborov [LICENSE](LICENSE) a [gpl.txt](gpl.txt). Priložené runtime
súbory sú samostatné runtime súbory priložené k tomuto forku. Hlasové doplnky
a používateľské licenčné súbory nie sú súčasťou balíka.
