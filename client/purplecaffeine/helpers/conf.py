"""Configuration info."""
from typing import List, Any


class Configuration:
    """Configuration list."""

    MAX_SIZE: float = 5e6

    @classmethod
    def all(cls) -> List[Any]:
        """Returns all Configurations."""
        return [Configuration.MAX_SIZE]
