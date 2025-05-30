"""Time estimate value object."""

from dataclasses import dataclass
from enum import Enum
from typing import Self


class TimeUnit(str, Enum):
    """Time units for estimates."""
    
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"


@dataclass(frozen=True)
class TimeEstimate:
    """Immutable time estimate value object."""
    
    value: float
    unit: TimeUnit
    
    def __post_init__(self) -> None:
        """Validate the estimate."""
        if self.value <= 0:
            raise ValueError(f"Time estimate must be positive, got {self.value}")
    
    @classmethod
    def minutes(cls, value: float) -> Self:
        """Create an estimate in minutes."""
        return cls(value, TimeUnit.MINUTES)
    
    @classmethod
    def hours(cls, value: float) -> Self:
        """Create an estimate in hours."""
        return cls(value, TimeUnit.HOURS)
    
    @classmethod
    def days(cls, value: float) -> Self:
        """Create an estimate in days."""
        return cls(value, TimeUnit.DAYS)
    
    @classmethod
    def weeks(cls, value: float) -> Self:
        """Create an estimate in weeks."""
        return cls(value, TimeUnit.WEEKS)
    
    def to_hours(self) -> float:
        """Convert estimate to hours."""
        conversions = {
            TimeUnit.MINUTES: self.value / 60,
            TimeUnit.HOURS: self.value,
            TimeUnit.DAYS: self.value * 8,  # Assuming 8-hour workday
            TimeUnit.WEEKS: self.value * 40,  # Assuming 40-hour workweek
        }
        return conversions[self.unit]
    
    def __str__(self) -> str:
        """String representation of the estimate."""
        return f"{self.value} {self.unit.value}"
