# Back_und_Koch

Individuelles Bestellsystem für Lebensmittel mit Offline-Verwaltung.

## Überblick

Streamlit-Anwendung mit REST-API und lokaler SQLite-Datenbank. Das System läuft komplett offline und lässt sich unter Windows per Batch-Datei einrichten und starten.

## Tech-Stack

- Python
- Streamlit (Oberfläche)
- REST-API
- SQLAlchemy + SQLite

## Projektstruktur

```text
├── app.py                 # Streamlit-App
├── app_main.py            # Haupteinstieg
├── pages/                 # Streamlit-Seiten
├── rest_api/              # REST-API
├── requirements.txt
├── setup_offline.bat      # Offline-Einrichtung
├── setup_offline-big.bat  # Offline-Einrichtung (große Variante)
├── start.bat              # Start
└── start-big.bat          # Start (große Variante)
```

## Installation

**Windows (Offline-Setup):**

```bat
setup_offline.bat
```

**Manuell:**

```bash
git clone https://github.com/Busaschie/Back_und_Koch.git
cd Back_und_Koch
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Nutzung

```bat
start.bat
```

oder manuell:

```bash
streamlit run app.py
```

Die Oberfläche ist unter `http://localhost:8501` erreichbar.
