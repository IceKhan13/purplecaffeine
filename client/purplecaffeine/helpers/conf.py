"""Configuration info."""
from typing import List, Any


class Configuration:
    """Configuration list."""

    MAX_SIZE: float = 5e6
    API_TRIAL_ENDPOINT: str = "api/trials"
    API_TOKEN_ENDPOINT: str = "api/token"
    API_HEADERS: dict = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    API_TIMEOUT: int = 30

    @classmethod
    def all(cls) -> List[Any]:
        """Returns all Configurations."""
        return [
            Configuration.MAX_SIZE,
            Configuration.API_TRIAL_ENDPOINT,
            Configuration.API_TOKEN_ENDPOINT,
            Configuration.API_HEADERS,
            Configuration.API_TIMEOUT,
        ]
