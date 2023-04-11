"""Backend."""
from typing import Optional, Union

from purplecaffeine.backend import BaseBackend, LocalBackend


class Trial:
    """Trial class."""

    def __init__(self, name: str, backend: Optional[BaseBackend] = None):
        """Trail class for tracking experiments data.

        Args:
            name: name of trial
            backend: backend to store data of trial. Default: local storage.
        """
        self.name = name
        self.backend = backend or LocalBackend(path="./")

        self.metrics = []

    def add_metric(self, name: str, value: Union[int, float]):
        """Adds metric to trial data.

        Args:
            name: name of metric
            value: value of metric
        """
        self.metrics.append((name, value))

    def __repr__(self):
        return f"<Trial: {self.name}>"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.backend.save_trial(self)
