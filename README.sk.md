# 32-bitový most Vocalizer Automotive pre NVDA

[English](README.md) | [Polski](README.pl.md) | Slovenčina

Projekt upravuje starší 32-bitový ovládač Nuance Vocalizer Automotive 5.5
tak, aby fungoval v 32-bitových aj 64-bitových verziách NVDA.

V 32-bitovom NVDA sa pôvodný ovládač Automotive načíta priamo. V
64-bitovom NVDA ho most spúšťa vo vyhradenom 32-bitovom hostiteľovi
syntetizátora. Spôsob odovzdávania zvuku reči závisí od nainštalovaného
variantu: štandardného alebo brokered audio.

## Dôležité

Balík neobsahuje samostatné hlasové doplnky Vocalizer ani používateľský súbor
`vocalizer_license.ini`. Runtime stále vyžaduje platnú licenciu, ktorú treba
importovať samostatne.

Tento fork je udržiavaný nezávisle. Problémy hláste v tomto úložisku a žiadosti o podporu neposielajte dodávateľom ani správcom pôvodných komponentov. Pôvodný projekt Vocalizer Automotive 5.5 sa už oficiálne nevyvíja ani nepodporuje. Pôvodný autor doplnku nezodpovedá za tento nezávislý fork, zmeny v ňom ani technickú podporu.

## Odporúčané súbory na stiahnutie

### Vocalizer Automotive 2.1.7 — Classic bridge

[Stiahnuť Vocalizer Automotive 2.1.7](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.1.7/vocalizer_automotive_driver-2.1.7.nvda-addon)

Toto je odporúčaný variant na bežné každodenné používanie. V 64-bitovom NVDA
používa klasický most kompatibility a podporuje NVDA 2026.1 a novšie. V
32-bitovom NVDA používa natívny priamy ovládač Automotive.

### Vocalizer Automotive 2.2.0-2026-08-03 — Brokered audio

[Stiahnuť experimentálny variant brokered audio](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.2.0-2026-08-03/vocalizer_automotive_driver-2.2.0-2026-08-03.nvda-addon)

Tento experimentálny variant je určený pre 64-bitové NVDA 2026.2 a novšie.
Odovzdáva zvuk z 32-bitového hostiteľa cez hlavný zvukový proces NVDA, čo na
podporovanej ceste umožňuje napríklad natívne stíšenie zvuku NVDA a
kompatibilitu so Sonic Pitch. Obsahuje známe problémy so zrušením a radením
reči do frontu, preto sa na bežné používanie naďalej odporúča verzia 2.1.7.

### Vocalizer Automotive 2.1.6 — oprava kompatibility pre NVDA 2025

[Stiahnuť verziu kompatibility pre NVDA 2025](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.1.6-nvda2025/vocalizer_automotive_driver-2.1.6-2025fix.nvda-addon)

Ide o osobitnú opravu kompatibility pre natívne 32-bitové NVDA 2025.x,
založenú na Vocalizer Automotive 2.1.6. **Nie je** to pôvodné vydanie
Vocalizer Automotive 2.1.6 od spoločnosti Tiflotecnia a neobsahuje most pre
64-bitové NVDA.

Staršie vydania označené dátumom zostávajú dostupné na historické a archívne
účely. Väčšina používateľov by si mala vybrať jednu z troch vyššie uvedených
verzií.

## Inštalácia

1. Vyberte vhodný variant v časti **Odporúčané súbory na stiahnutie** a
   nainštalujte jeho súbor `.nvda-addon`. Ak používate priamo zdrojový strom,
   skopírujte obsah priečinka `addon` — nie samotný priečinok `addon` — do
   priečinka doplnkov NVDA.
2. Balík už obsahuje požadované runtime súbory Automotive.
3. Samostatne nainštalujte vlastné doplnky s hlasmi Vocalizer Automotive.
   Ich priečinky sa zvyčajne začínajú na `vocalizer-voice-`.
4. Spustite NVDA a otvorte:

   `Ponuka NVDA > Vocalizer Automotive > Zadať licenciu`

   Licencia sa skopíruje do:

   `%APPDATA%\nvda\vocalizer_license.ini`

5. Reštartujte NVDA a vyberte ovládač podľa architektúry NVDA:

   - 32-bitové NVDA: `vocalizerAutomotive`
   - 64-bitové NVDA: `vocalizerAutomotive32`

## Spracovanie zvuku

Štandardný variant používa klasický most kompatibility NVDA v 64-bitovom
NVDA. V 32-bitovom NVDA používa Automotive natívnu priamu cestu. Sonic Pitch
so štandardným variantom nefunguje.

Ak chcete odovzdávať zvuk cez hlavný proces NVDA a používať natívne
stíšenie zvuku NVDA a kompatibilitu so Sonic Pitch v podporovaných
64-bitových verziách NVDA, nainštalujte variant brokered audio.

## Dostupné varianty

- **Classic bridge — 2.1.7:** odporúčaná verzia na všeobecné používanie. V
  64-bitovom NVDA 2026.1 a novšom načítava 32-bitový ovládač cez klasický
  most kompatibility NVDA a v 32-bitovom NVDA ho načítava priamo.
- **Brokered audio — 2.2.0-2026-08-03:** experimentálna verzia pre 64-bitové
  NVDA 2026.2 a novšie. Odovzdáva zvuk reči z 32-bitového hostiteľa cez
  hlavný zvukový proces NVDA. V 32-bitovom NVDA používa natívnu priamu cestu.
- **Legacy NVDA 2025 compatibility fix — 2.1.6-nvda2025:** natívna 32-bitová
  verzia pre NVDA 2025.x. Neobsahuje most pre 64-bitové NVDA a nie je
  pôvodným vydaním Tiflotecnie 2.1.6.

Naraz inštalujte iba jeden variant.

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
`addon/locale/vocalizer_automotive_driver.pot`.

Rozhranie doplnku obsahuje lokalizácie: `an`, `ar`, `da`, `de`, `el`, `es`,
`fi`, `fr`, `gl`, `hr`, `hu`, `it`, `ja`, `ko`, `nb_NO`, `ne`, `nl`, `pl`,
`pt_BR`, `pt_PT`, `ru`, `sk`, `sl`, `tr` a `zh_CN`. HTML dokumentácia je
dostupná v angličtine, poľštine a slovenčine.

## Licencia

Zdrojový kód ovládača NVDA a mosta je distribuovaný pod licenciou GPL-2.0
podľa súboru [gpl.txt](addon/gpl.txt). Priložené runtime súbory sú samostatné runtime
súbory priložené k tomuto forku. Hlasové doplnky a používateľské licenčné
súbory nie sú súčasťou balíka.
