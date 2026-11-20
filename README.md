# Fordonsdata – testautomatisering för simulerad telemetri

Ett Python-verktyg som kontrollerar CSV-loggar med simulerade hastighetsmätningar från ett fordon. Verktyget hittar luckor i paketens löpnummer, tidsstämplar som går bakåt och serier av identiska hastighetsvärden som kan tyda på en fastnad sensor.

## Kör demon

Kör från projektets rot med Python 3.12.

```cmd
py validate.py
```

På macOS och Linux använder du `python3` i stället för `py`.

Exempelfilen `telemetry.csv` innehåller tre avsiktliga avvikelser. Förväntad utskrift:

```text
Saknat paket: 103
Paket 102: tidsstämpeln gick bakåt från 100 till 80 ms
Paket 108: misstänkt fastnad hastighet (43.0 km/h i fem paket i rad)
```

## Vad kontrolleras?

| Kontroll | Regel |
| --- | --- |
| Saknade paket | Ett hopp i `sequence_id` flaggar löpnumren i luckan. Kontrollen förutsätter en enda dataström där paketen kommer i löpnummerordning. |
| Felordnade tidsstämplar | Ett paket flaggas om `timestamp_ms` är lägre än i föregående paket. |
| Misstänkt fastnad hastighet | Fem identiska `speed_kmh`-värden i rad ger en flagga vid den femte mätningen. Konstant fart kan också ge samma värde, så kontrollen används som en indikator. |

## Kör testerna

```cmd
py -m pip install pytest
py -m pytest -q
```

Testsviten innehåller åtta tester för giltiga mätserier och avvikelser. [GitHub Actions](.github/workflows/tests.yml) kör testerna med Python 3.12 vid push och pull requests.

## Projektfiler

- [`validate.py`](validate.py) läser CSV-filen och rapporterar avvikelser.
- [`telemetry.csv`](telemetry.csv) innehåller de simulerade mätpaketen.
- [`test_validate.py`](test_validate.py) innehåller enhetstester för de tre kontrollerna.
