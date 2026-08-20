# Most 32-bitowego Vocalizer Automotive dla NVDA

[English](README.md) | Polski | [Slovenčina](README.sk.md)

Projekt dostosowuje starszy, 32-bitowy sterownik Nuance Vocalizer Automotive
5.5 do 32- i 64-bitowych wersji NVDA.

W 32-bitowym NVDA oryginalny sterownik Automotive jest ładowany
bezpośrednio. W 64-bitowym NVDA most uruchamia go w dedykowanym 32-bitowym
hoście syntezatora. Sposób przekazywania dźwięku mowy zależy od zainstalowanego
wariantu: standardowego albo brokered audio.

## Ważne

Pakiet nie zawiera osobnych dodatków z głosami Vocalizer ani przypisanego do
użytkownika pliku `vocalizer_license.ini`. Runtime nadal wymaga ważnej
licencji, którą należy zaimportować osobno.

Ten fork jest utrzymywany niezależnie. Zgłaszaj problemy w tym repozytorium i nie kieruj próśb o pomoc do dostawców ani opiekunów oryginalnych komponentów. Oryginalny projekt Vocalizer Automotive 5.5 nie jest już oficjalnie rozwijany ani wspierany. Autor oryginalnego dodatku nie ponosi odpowiedzialności za ten niezależny fork, wprowadzone w nim modyfikacje ani pomoc techniczną.

## Zalecane wersje do pobrania

### Vocalizer Automotive 2.1.7 — Classic bridge

[Pobierz Vocalizer Automotive 2.1.7](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.1.7/vocalizer_automotive_driver-2.1.7.nvda-addon)

Jest to wariant zalecany do normalnego, codziennego użycia. W 64-bitowym NVDA
używa klasycznego mostu zgodności i obsługuje NVDA 2026.1 oraz nowsze wersje.
W 32-bitowym NVDA korzysta z natywnego, bezpośredniego sterownika Automotive.

### Vocalizer Automotive 2.2.0-2026-08-03 — Brokered audio

[Pobierz eksperymentalny wariant brokered audio](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.2.0-2026-08-03/vocalizer_automotive_driver-2.2.0-2026-08-03.nvda-addon)

Ten eksperymentalny wariant jest przeznaczony dla 64-bitowego NVDA 2026.2 i
nowszych wersji. Przekazuje dźwięk z 32-bitowego hosta przez główny proces
audio NVDA, co na obsługiwanej ścieżce umożliwia między innymi natywne
przyciszanie dźwięku NVDA oraz zgodność z Sonic Pitch. Występują w nim znane
problemy z anulowaniem i kolejkowaniem mowy, dlatego do zwykłego użycia nadal
zalecana jest wersja 2.1.7.

### Vocalizer Automotive 2.1.6 — poprawka zgodności dla NVDA 2025

[Pobierz wersję zgodnościową dla NVDA 2025](https://github.com/kazek5p-git/vocalizer-automotive-32bit-bridge/releases/download/v2.1.6-nvda2025/vocalizer_automotive_driver-2.1.6-2025fix.nvda-addon)

Jest to specjalna poprawka zgodności dla natywnego 32-bitowego NVDA 2025.x,
oparta na Vocalizer Automotive 2.1.6. **Nie** jest to oryginalne wydanie
Vocalizer Automotive 2.1.6 opublikowane przez Tiflotecnię i nie zawiera mostu
dla 64-bitowego NVDA.

Starsze wydania oznaczone datami pozostają dostępne do celów historycznych i
archiwalnych. Większość użytkowników powinna wybrać jedną z trzech powyższych
wersji.

## Instalacja

1. Wybierz odpowiedni wariant w sekcji **Zalecane wersje do pobrania** i
   zainstaluj jego plik `.nvda-addon`. Jeżeli korzystasz bezpośrednio z kodu
   źródłowego, skopiuj zawartość katalogu `addon` — bez samego katalogu
   `addon` — do katalogu dodatków NVDA.
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

Wariant standardowy używa klasycznego mostu zgodności NVDA w 64-bitowym
NVDA. W 32-bitowym NVDA Automotive korzysta z natywnej ścieżki bezpośredniej.
Sonic Pitch nie działa z wariantem standardowym.

Aby przekazywać dźwięk przez główny proces NVDA oraz korzystać z natywnego
przyciszania dźwięku NVDA i zgodności z Sonic Pitch w obsługiwanych
64-bitowych wersjach NVDA, zainstaluj wariant brokered audio.

## Dostępne warianty

- **Classic bridge — 2.1.7:** zalecana wersja ogólnego przeznaczenia. W
  64-bitowym NVDA 2026.1 i nowszym ładuje 32-bitowy sterownik przez klasyczny
  most zgodności NVDA, a w 32-bitowym NVDA ładuje go bezpośrednio.
- **Brokered audio — 2.2.0-2026-08-03:** eksperymentalna wersja dla
  64-bitowego NVDA 2026.2 i nowszego. Przekazuje dźwięk mowy z 32-bitowego
  hosta przez główny proces audio NVDA. W 32-bitowym NVDA korzysta z natywnej
  ścieżki bezpośredniej.
- **Legacy NVDA 2025 compatibility fix — 2.1.6-nvda2025:** natywna 32-bitowa
  wersja dla NVDA 2025.x. Nie zawiera mostu dla 64-bitowego NVDA i nie jest
  oryginalnym wydaniem Tiflotecnii 2.1.6.

Instaluj tylko jeden wariant naraz.

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
`addon/locale/vocalizer_automotive_driver.pot`.

Interfejs dodatku zawiera lokalizacje: `an`, `ar`, `da`, `de`, `el`, `es`, `fi`,
`fr`, `gl`, `hr`, `hu`, `it`, `ja`, `ko`, `nb_NO`, `ne`, `nl`, `pl`, `pt_BR`,
`pt_PT`, `ru`, `sk`, `sl`, `tr` i `zh_CN`. Dokumentacja HTML jest dostępna po
angielsku, polsku i słowacku.

## Licencja

Kod sterownika NVDA i mostu jest udostępniany na licencji GPL-2.0, zgodnie
z plikiem [gpl.txt](addon/gpl.txt). Dołączone pliki runtime są
osobnymi plikami runtime dołączonymi do tego fork’a. Dodatki z głosami i
przypisane do użytkownika pliki licencji nie są dołączane.
