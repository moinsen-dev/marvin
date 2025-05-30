"""Task priority value object."""

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, order=True)
class TaskPriority:
    """Immutable task priority value object."""
    
    value: int  # 0-100, higher is more important
    
    def __post_init__(self) -> None:
        """Validate the priority value."""
        if not 0 <= self.value <= 100:
            raise ValueError(f"Priority must be between 0 and 100, got {self.value}")
    
    @classmethod
    def critical(cls) -> Self:
        """Create a critical priority."""
        return cls(100)
    
    @classmethod
    def high(cls) -> Self:
        """Create a high priority."""
        return cls(75)
    
    @classmethod
    def medium(cls) -> Self:
        """Create a medium priority."""
        return cls(50)
    
    @classmethod
    def low(cls) -> Self:
        """Create a low priority."""
        return cls(25)
    
    @classmethod
    def trivial(cls) -> Self:
        """Create a trivial priority."""
        return cls(10)
    
    def __str__(self) -> str:
        """String representation of priority."""
        if self.value >= 90:
            return "Critical"
        elif self.value >= 70:
            return "High"
        elif self.value >= 40:
            return "Medium"
        elif self.value >= 20:
            return "Low"
        else:
            return "Trivial"
