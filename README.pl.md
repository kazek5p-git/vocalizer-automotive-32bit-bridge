# Vocalizer Automotive 2.1.6 – wersja zgodnościowa dla NVDA 2025

[English](README.md) | Polski | [Slovenčina](README.sk.md)

Ta gałąź zachowuje oryginalny, natywny 32-bitowy sterownik Vocalizer
Automotive 5.5 wydany przez Tiflotecnię jako wersja 2.1.6, z niewielką
poprawką zgodności dla NVDA 2025.x.

Jest ona celowo oddzielona od prac nad 32-bitowym mostem prowadzonych
w gałęziach `main` i `brokered-audio`.

## Przeznaczenie

Vocalizer Automotive jest natywnym 32-bitowym syntezatorem. Ta gałąź jest
przeznaczona dla użytkowników, którzy nadal korzystają z 32-bitowej wersji
NVDA i chcą zachować oryginalne działanie sterownika bez używania mostu
zgodności wymaganego przez 64-bitowe NVDA.

Pozwala to zachować oryginalną integrację i zachowanie Automotive, w tym
natywną obsługę licencji i komunikaty licencyjne.

## Zgodność

- Tylko natywne 32-bitowe NVDA
- Przeznaczona dla NVDA 2025.x
- Nie zawiera 32-bitowego mostu dla 64-bitowego NVDA
- Dla aktualnych 64-bitowych wersji NVDA należy użyć gałęzi `main` lub
  `brokered-audio`

## Zmiany względem Vocalizer Automotive 2.1.6

Silnik syntezy ani normalne zachowanie sterownika Vocalizer nie zostały
przebudowane.

Główna poprawka zgodności dotyczy wykrywania urządzenia wyjściowego audio:

- NVDA 2025.1 i nowsze: odczytywane jest `audio.outputDevice`
- Starsze wersje NVDA: używany jest zapasowo starszy
  `speech.outputDevice`
- Jeżeli żadna z tych wartości konfiguracji nie jest dostępna, używane
  jest domyślne urządzenie audio

Pakiet zawiera również utrzymywane tłumaczenia polskie i słowackie oraz
zamierzone aktualizacje lokalizacji zachowane w tej gałęzi archiwalnej.

Zmodyfikowany plik `_vocalizer.py` zawiera wyraźną informację wskazującą
DJ Graco jako autora poprawki zgodności dla NVDA 2025.

## Ważne

Nie jest to oficjalne wydanie Tiflotecnii. Jest to wersja zachowawcza
i zgodnościowa oparta na ostatnim sterowniku Tiflotecnii w wersji 2.1.6.

Nadal wymagane są ważna licencja Vocalizer Automotive oraz zgodne dodatki
z głosami. Przypisane do użytkownika pliki licencji ani oddzielne pakiety
głosów nie są udostępniane w tym repozytorium.

Oryginalny projekt Vocalizer Automotive nie jest już oficjalnie rozwijany
ani wspierany przez Tiflotecnię.

## Pozostałe gałęzie

- `main` – Vocalizer Automotive 2.1.7 Classic bridge
- `brokered-audio` – eksperymentalna wersja brokered audio dla współczesnego
  64-bitowego NVDA
- `legacy-2.1.6-2025` – natywna 32-bitowa wersja 2.1.6 dostosowana do
  NVDA 2025.x

## Licencja

Kod źródłowy sterownika NVDA jest rozpowszechniany na warunkach GNU General
Public License zgodnie z plikiem [gpl.txt](addon/gpl.txt).
