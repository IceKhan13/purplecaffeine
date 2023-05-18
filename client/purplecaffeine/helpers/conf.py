"""Configuration info."""
from typing import List, Any


class Configuration:
    """Configuration list."""

    MAX_SIZE: float = 5e6
    API_HTTP: str = "http"
    API_URL: str = "127.0.0.1"
    API_PORT: str = "8000"
    API_TRIAL_ENDPOINT: str = "api/trials"
    API_FULL_URL: str = f"{API_HTTP}://{API_URL}:{API_PORT}/{API_TRIAL_ENDPOINT}"
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
            Configuration.API_HTTP,
            Configuration.API_URL,
            Configuration.API_PORT,
            Configuration.API_TRIAL_ENDPOINT,
            Configuration.API_FULL_URL,
            Configuration.API_HEADERS,
            Configuration.API_TIMEOUT,
        ]
