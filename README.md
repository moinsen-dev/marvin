# Marvin

> "Life? Don't talk to me about life." - Marvin, the Paranoid Android

## Überblick

Marvin ist ein intelligentes Tool, das Produktanforderungsdokumente (PRDs) analysiert und diese in strukturierte AI-Coding-Tasks umwandelt. Benannt nach dem depressiven Roboter aus "Per Anhalter durch die Galaxis" hilft Marvin Entwicklern, ihre Projekte effizienter zu organisieren und AI-Coding-Assistenten (wie Cursor, Windsurf oder Claude Code) optimal zu nutzen.

## Funktionen

- **PRD-Analyse**: Extraktion von Features und Anforderungen aus Produktanforderungsdokumenten
- **Codebase-Scanning**: Analyse bestehender Codebases zur Integration neuer Features
- **Template-Generierung**: Erstellung strukturierter AI-Coding-Task-Templates im XML-Format
- **Sequenzplanung**: Automatische Aufteilung von Anforderungen in logische, aufeinander aufbauende Aufgaben

## Interfaces

Marvin bietet drei verschiedene Zugriffsmethoden:

1. **CLI-Tool**: Für Entwickler, die Marvin direkt in ihrer lokalen Umgebung nutzen möchten
2. **API**: Für die Integration in CI/CD-Pipelines und andere Tools
3. **MCP-Server**: Für kollaborative Entwicklungsumgebungen und komplexe Anwendungsfälle

## Technologie

- Python 3.11+
- FastAPI
- Google ADK (Agent Development Kit)
- Context 7 für Codeanalyse
- Agenten-basierte Architektur

## Installation

```bash
# Mit Poetry (empfohlen)
poetry install

# Mit pip
pip install -e .
```

## Schnellstart

```bash
# Als CLI-Tool
marvin analyze --prd path/to/prd.md --output path/to/output

# Als API-Server starten
marvin serve-api

# Als MCP-Server starten
marvin serve-mcp
```

## Projektstruktur

```
/marvin
  /src
    /core          # Domänenlogik
    /adapters      # Interfaces (CLI, API, MCP)
    /infrastructure # Technische Implementierungen
  /tests
  /docs
  /examples
```

## Lizenz

MIT

## Hinweis

*Don't Panic!* - Auch wenn Marvin manchmal depressiv sein mag, ist er immer hier, um zu helfen.
