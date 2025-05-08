import functools
import sys
import time
import traceback
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Generator, Optional, TypeVar

from loguru import logger


def setup_logging(log_level: str = "INFO") -> None:
    """
    Set up logging for the application.

    Args:
        log_level (str): The log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Remove default handler
    logger.remove()

    # Add a handler for stdout with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Add a handler for a rotating file
    logger.add(
        "logs/marvin.log",
        rotation="10 MB",
        retention="1 week",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
    )


def get_logger(name: str) -> Any:
    """
    Get a logger for a specific module.

    Args:
        name (str): Name of the module

    Returns:
        Logger: A logger instance with the module name bound to it
    """
    return logger.bind(name=name)


def log_exception(
    logger_instance: Any, message: str, exc: Exception, level: str = "ERROR"
) -> None:
    """
    Log an exception with detailed traceback information.

    Args:
        logger_instance: Logger instance to use for logging
        message: Message to log
        exc: Exception to log
        level: Log level to use
    """
    tb_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    log_message = f"{message}: {str(exc)}\n{tb_str}"
    logger_instance.log(level, log_message)


# Type variable for function return type
T = TypeVar("T")


@contextmanager
def log_time(logger_instance: Any, operation: str) -> Generator[None, None, None]:
    """
    Context manager for timing operations and logging the duration.

    Args:
        logger_instance: Logger instance to use for logging
        operation: Name of the operation being timed

    Yields:
        None
    """
    start_time = time.time()
    logger_instance.info(f"Starting {operation}")
    try:
        yield
        elapsed_time = time.time() - start_time
        logger_instance.info(f"Completed {operation} in {elapsed_time:.2f}s")
    except Exception as e:
        elapsed_time = time.time() - start_time
        log_exception(
            logger_instance, f"Error in {operation} after {elapsed_time:.2f}s", e
        )
        raise


def log_function_time(logger_instance: Optional[Any] = None) -> Callable:
    """
    Decorator for timing function execution and logging the duration.

    Args:
        logger_instance: Optional logger instance. If None, will get a logger with the function's module name.

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Get the module name from the function if no logger provided
            nonlocal logger_instance
            if logger_instance is None:
                logger_instance = get_logger(func.__module__)

            start_time = time.time()
            logger_instance.debug(f"Calling {func.__name__}")
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                logger_instance.debug(
                    f"Completed {func.__name__} in {elapsed_time:.2f}s"
                )
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                log_exception(
                    logger_instance,
                    f"Error in {func.__name__} after {elapsed_time:.2f}s",
                    e,
                )
                raise

        return wrapper

    return decorator
