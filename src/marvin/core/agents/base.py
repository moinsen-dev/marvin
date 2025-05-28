"""Base class for Marvin agents."""

import abc
import time
from typing import Any

from marvin.logging import get_logger


class Agent(abc.ABC):
    """Abstract base class for all Marvin agents."""

    def __init__(self, name: str, config: dict[str, Any] | None = None):
        """Initializes an agent.

        Args:
            name: Name of the agent
            config: Configuration of the agent
        """
        self.name = name
        self.config = config or {}
        self.logger = get_logger(f"agent.{name}")
        self.logger.debug(
            f"Initialized {self.__class__.__name__} with config: {self.config}"
        )

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

    async def _timed_execute(self, *args: Any, **kwargs: Any) -> Any:
        """Executes the main function of the agent with timing and logging.

        Args:
            *args: Arguments for execution
            **kwargs: Keyword arguments for execution

        Returns:
            The result of the execution
        """
        self.logger.info(
            f"Executing {self.__class__.__name__} with args: {args}, kwargs: {kwargs}"
        )
        start_time = time.time()
        try:
            result = await self.execute(*args, **kwargs)
            elapsed_time = time.time() - start_time
            self.logger.info(
                f"Completed {self.__class__.__name__} execution in {elapsed_time:.2f}s"
            )
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error(
                f"Error executing {self.__class__.__name__} after {elapsed_time:.2f}s: {str(e)}"
            )
            raise

    def get_config(self, key: str, default: Any = None) -> Any:
        """Returns a configuration value.

        Args:
            key: Key of the configuration value
            default: Default value if the key does not exist

        Returns:
            The configuration value or the default value
        """
        value = self.config.get(key, default)
        self.logger.debug(f"Retrieved config {key}={value}")
        return value

    def set_config(self, key: str, value: Any) -> None:
        """Sets a configuration value.

        Args:
            key: Key of the configuration value
            value: Value of the configuration value
        """
        self.logger.debug(f"Setting config {key}={value}")
        self.config[key] = value

    def __str__(self) -> str:
        """String representation of the agent.

        Returns:
            String representation
        """
        return f"{self.__class__.__name__}(name={self.name})"
