# Marvin - Installationsanleitung

In dieser Anleitung wird beschrieben, wie du Marvin lokal installierst und mit der Entwicklung beginnst.

## Voraussetzungen

- Python 3.11 oder höher
- Poetry (für Dependency-Management)
- Git

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/yourusername/marvin.git
cd marvin
```

### 2. Virtuelle Umgebung einrichten mit Poetry

```bash
# Poetry installieren (falls noch nicht vorhanden)
curl -sSL https://install.python-poetry.org | python3 -

# Abhängigkeiten installieren
poetry install
```

### 3. Entwicklungsumgebung aktivieren

```bash
poetry shell
```

## Verwendung

Marvin kann auf drei verschiedene Arten verwendet werden:

### 1. Als CLI-Tool

```bash
# Hilfe anzeigen
marvin --help

# Ein PRD analysieren und AI-Coding-Tasks generieren
marvin analyze path/to/prd.md --output ./output-dir

# Mit Codebase-Analyse
marvin analyze path/to/prd.md --codebase path/to/codebase --output ./output-dir
```

### 2. Als API-Server

```bash
# API-Server starten
marvin serve-api

# Mit benutzerdefiniertem Host und Port
marvin serve-api --host 0.0.0.0 --port 8080
```

Die API ist dann unter `http://localhost:8000` (bzw. dem angegebenen Host/Port) erreichbar.

### 3. Als MCP-Server

```bash
# MCP-Server starten
marvin serve-mcp

# Mit benutzerdefiniertem Host und Port
marvin serve-mcp --host 0.0.0.0 --port 9090
```

## Entwicklung

### Tests ausführen

```bash
# Alle Tests ausführen
pytest

# Mit Coverage-Bericht
pytest --cov=marvin

# Nur Unit-Tests
pytest tests/unit
```

### Code formatieren

```bash
# Code formatieren mit Black
black src tests

# Imports sortieren mit isort
isort src tests
```

### Linting

```bash
# Code prüfen mit Ruff
ruff check src tests
```

## Konfiguration

Marvin kann über Umgebungsvariablen konfiguriert werden:

- `MARVIN_API_HOST` - Host für den API-Server
- `MARVIN_API_PORT` - Port für den API-Server
- `MARVIN_MCP_HOST` - Host für den MCP-Server
- `MARVIN_MCP_PORT` - Port für den MCP-Server
- `MARVIN_CONTEXT7_API_KEY` - API-Key für Context 7
- `MARVIN_LOG_LEVEL` - Log-Level (INFO, DEBUG, WARNING, ERROR)
- `MARVIN_ENVIRONMENT` - Umgebung (development, production)

Beispiel:

```bash
export MARVIN_LOG_LEVEL=DEBUG
export MARVIN_ENVIRONMENT=development
marvin analyze path/to/prd.md
```

## Beispiel-PRD verwenden

Im `examples`-Verzeichnis findest du ein Beispiel-PRD:

```bash
marvin analyze examples/prd/example_prd.md
```

## Fehlersuche

Falls Probleme auftreten, prüfe Folgendes:

1. Ist Python 3.11 oder höher installiert? `python --version`
2. Ist Poetry installiert? `poetry --version`
3. Wurden alle Abhängigkeiten installiert? `poetry show`
4. Ist die virtuelle Umgebung aktiviert? `poetry env info`

## Nächste Schritte

- Implementiere einen eigenen Agenten
- Füge neue Features hinzu
- Verbessere die Dokumentation
- Trage zur Projektentwicklung bei
