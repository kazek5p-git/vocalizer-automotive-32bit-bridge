# Most 32-bitowego Vocalizer Automotive dla NVDA

[English](README.md) | Polski | [Slovenčina](README.sk.md)

Projekt dostosowuje starszy, 32-bitowy sterownik Nuance Vocalizer Automotive
5.5 do współczesnych 64-bitowych wersji NVDA.

Most uruchamia oryginalny sterownik 32-bitowy w dedykowanym hoście
syntezatora NVDA. Dźwięk jest przekazywany z powrotem do głównego procesu
NVDA, dzięki czemu dodatki przetwarzające mowę mogą go odbierać.

## Ważne

To repozytorium celowo nie zawiera:

- `vautov5.dll`
- `nuan_platform.dll`
- danych głosowych Vocalizer
- plików licencji Vocalizer

Są to pliki własnościowe lub objęte licencją. Użyj własnej, legalnie nabytej
kopii. Nie przesyłaj ich do tego repozytorium.

Projekt nie jest powiązany z NV Access, Tiflotecnia, Nuance ani Cerence.

## Instalacja

1. Zainstaluj publiczny plik `.nvda-addon` z zakładki GitHub Releases albo
   skopiuj repozytorium do katalogu dodatków NVDA.
2. Umieść własne biblioteki runtime w katalogu:

   `%APPDATA%\nvda\addons\vocalizer_automotive_driver\synthDrivers\vocalizerAutomotive\common\speech\components`

   Wymagane pliki:

   - `vautov5.dll`
   - `nuan_platform.dll`

3. Zainstaluj osobno własne dodatki z głosami Vocalizer Automotive. Ich
   katalogi zwykle zaczynają się od `vocalizer-voice-`.
4. Uruchom NVDA i otwórz:

   `Menu NVDA > Ustawienia > Vocalizer Automotive > Wprowadź licencję`

   Licencja zostanie skopiowana do:

   `%APPDATA%\nvda\vocalizer_license.ini`

5. Uruchom ponownie NVDA i wybierz syntezator:

   `vocalizerAutomotive32`

## Automatyczne przełączanie języka

W menu znajduje się pozycja **Ustawienia automatycznego przełączania języka**.
Okno wykrywa zainstalowane głosy Automotive na podstawie metadanych `.hdr`
i zapisuje wybrane przypisania głosów w:

`%APPDATA%\nvda\vocalizer.ini`

## Sprawdzenie środowiska

Uruchom:

```powershell
.\tools\Check-VocalizerAutomotiveRuntime.ps1
```

Skrypt pokazuje brakujące biblioteki runtime i wykryte dodatki głosowe. Nie
pobiera ani nie dołącza plików własnościowych.

## Budowanie

Aby zbudować publiczny dodatek bez plików runtime:

```powershell
.\tools\Build-PublicAddon.ps1
```

Pakiet zostanie zapisany w katalogu `dist`.

Uniwersalny szablon tłumaczeń znajduje się w pliku
`locale/vocalizer_automotive_driver.pot`.

## Licencja

Kod sterownika NVDA i mostu jest udostępniany na licencji GPL-2.0, zgodnie
z plikami [LICENSE](LICENSE) i [gpl.txt](gpl.txt). Licencja ta nie daje prawa
do rozpowszechniania zewnętrznych bibliotek Vocalizer, danych głosowych ani
plików licencji.
