"""Base class for Marvin agents."""

import abc
from typing import Any, Dict, List, Optional


class Agent(abc.ABC):
    """Abstract base class for all Marvin agents."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initializes an agent.
        
        Args:
            name: Name of the agent
            config: Configuration of the agent
        """
        self.name = name
        self.config = config or {}
    
    @abc.abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Executes the main function of the agent.
        
        Args:
            *args: Arguments for execution
            **kwargs: Keyword arguments for execution
            
        Returns:
            The result of the execution
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Returns a configuration value.
        
        Args:
            key: Key of the configuration value
            default: Default value if the key does not exist
            
        Returns:
            The configuration value or the default value
        """
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Sets a configuration value.
        
        Args:
            key: Key of the configuration value
            value: Value of the configuration value
        """
        self.config[key] = value
    
    def __str__(self) -> str:
        """String representation of the agent.
        
        Returns:
            String representation
        """
        return f"{self.__class__.__name__}(name={self.name})"
