# Most 32-bitowego Vocalizer Automotive dla NVDA

[English](README.md) | Polski | [Slovenčina](README.sk.md)

Projekt dostosowuje starszy, 32-bitowy sterownik Nuance Vocalizer Automotive
5.5 do 32- i 64-bitowych wersji NVDA.

W 32-bitowym NVDA oryginalny sterownik Automotive jest ładowany bezpośrednio.
W 64-bitowym NVDA most uruchamia go w dedykowanym 32-bitowym hoście
syntezatora.

W 64-bitowym NVDA 2026.2 i nowszych ta gałąź używa ścieżki brokered audio
NVDA. Klasyczny bridge dla 64-bitowego NVDA znajduje się w wydaniu `v2.1.7`.

## Ważne

Pakiet zawiera kod mostu oraz pliki runtime wymagane przez 32-bitowy host
Automotive:

- `vautov5.dll`
- `nuan_platform.dll`
- `nuan_platform.dllz`
- wymagane dane komponentów i pliki strojenia

Pakiet nie zawiera osobnych dodatków z głosami Vocalizer ani przypisanego do
użytkownika pliku `vocalizer_license.ini`. Runtime nadal wymaga ważnej
licencji, którą należy zaimportować osobno.

Ten fork jest utrzymywany niezależnie. Zgłaszaj problemy w tym repozytorium
i nie kieruj próśb o pomoc do dostawców ani opiekunów oryginalnych komponentów.
Oryginalny projekt Vocalizer Automotive 5.5 jest abandonware, a autor
oryginalnego dodatku nie ponosi odpowiedzialności za ten fork ani jego pomoc
techniczną.

## Instalacja

1. Zainstaluj publiczny plik `.nvda-addon` z zakładki GitHub Releases albo
   skopiuj repozytorium do katalogu dodatków NVDA.
2. Pakiet zawiera już wymagane pliki runtime Automotive.
3. Zainstaluj osobno własne dodatki z głosami Vocalizer Automotive. Ich
   katalogi zwykle zaczynają się od `vocalizer-voice-`.
4. Uruchom NVDA i otwórz:

   `Menu NVDA > Vocalizer Automotive > Wprowadź licencję`

   Licencja zostanie skopiowana do:

   `%APPDATA%\nvda\vocalizer_license.ini`

5. Uruchom ponownie NVDA i wybierz sterownik odpowiedni dla architektury NVDA:

   - 32-bitowy NVDA: `vocalizerAutomotive`
   - 64-bitowy NVDA: `vocalizerAutomotive32`

## Przetwarzanie dźwięku

W 64-bitowym NVDA 2026.2 i nowszych wydanie używa usługi brokered audio NVDA,
aby przekazywać dźwięk mowy przez główny proces NVDA. W 32-bitowym NVDA
oryginalny sterownik Automotive korzysta z natywnej ścieżki bezpośredniej.
Sonic Pitch pozostaje zgodny ze ścieżką brokered audio.

Ten wariant obsługuje natywne przyciszanie dźwięku NVDA. Skrót
`Shift+NVDA+D` przełącza tryby przyciszania audio dostępne w NVDA. Wybrany tryb
jest zarządzany i zapisywany przez NVDA na brokered ścieżce 64-bitowej.
Klasyczny wariant `v2.1.7` nie korzysta z tej ścieżki brokered audio.

## Warianty wydań

- `v2.1.7`: klasyczny bridge dla 32-bitowego NVDA oraz 64-bitowego NVDA
  2026.1 i nowszych.
- `v2.2.0`: bridge brokered audio dla 64-bitowego NVDA 2026.2 i nowszych,
  z bezpośrednią ścieżką dla 32-bitowego NVDA.

Instaluj tylko jeden wariant dodatku naraz.

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

Skrypt pokazuje wymagane pliki runtime, wykryte dodatki głosowe oraz osobny
plik licencji. Nie pobiera ani nie dołącza licencji.

## Budowanie

Aby zbudować kompletny dodatek:

```powershell
.\tools\Build-PublicAddon.ps1
```

Pakiet zostanie zapisany w katalogu `dist` i będzie zawierał pliki runtime
przechowywane w repozytorium. Skrypt zawsze pomija `vocalizer_license.ini`.

Uniwersalny szablon tłumaczeń znajduje się w pliku
`locale/vocalizer_automotive_driver.pot`.

Interfejs dodatku zawiera lokalizacje: `an`, `ar`, `da`, `de`, `el`, `es`, `fi`,
`fr`, `gl`, `hr`, `hu`, `it`, `ja`, `ko`, `nb_NO`, `ne`, `nl`, `pl`, `pt_BR`,
`pt_PT`, `ru`, `sk`, `sl`, `tr` i `zh_CN`. Dokumentacja HTML jest dostępna po
angielsku, polsku i słowacku.

## Licencja

Kod sterownika NVDA i mostu jest udostępniany na licencji GPL-2.0, zgodnie
z plikami [LICENSE](LICENSE) i [gpl.txt](gpl.txt). Dołączone pliki runtime są
osobnymi plikami runtime dołączonymi do tego fork’a. Dodatki z głosami i
przypisane do użytkownika pliki licencji nie są dołączane.
