"""Basisklasse für Marvin-Agenten."""

import abc
from typing import Any, Dict, List, Optional


class Agent(abc.ABC):
    """Abstrakte Basisklasse für alle Marvin-Agenten."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialisiert einen Agenten.
        
        Args:
            name: Name des Agenten
            config: Konfiguration des Agenten
        """
        self.name = name
        self.config = config or {}
    
    @abc.abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Führt die Hauptfunktion des Agenten aus.
        
        Args:
            *args: Argumente für die Ausführung
            **kwargs: Keyword-Argumente für die Ausführung
            
        Returns:
            Das Ergebnis der Ausführung
        """
        raise NotImplementedError("Subklassen müssen execute() implementieren")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Gibt einen Konfigurationswert zurück.
        
        Args:
            key: Schlüssel des Konfigurationswerts
            default: Standardwert, falls der Schlüssel nicht existiert
            
        Returns:
            Der Konfigurationswert oder der Standardwert
        """
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Setzt einen Konfigurationswert.
        
        Args:
            key: Schlüssel des Konfigurationswerts
            value: Wert des Konfigurationswerts
        """
        self.config[key] = value
    
    def __str__(self) -> str:
        """String-Repräsentation des Agenten.
        
        Returns:
            String-Repräsentation
        """
        return f"{self.__class__.__name__}(name={self.name})"
