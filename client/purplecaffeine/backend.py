"""Backend."""


class BaseBackend:
    """Base backend class."""

    def save_trial(self, trial):
        """Saves given trial.

        Args:
            trial: trial to save
        """
        raise NotImplementedError


class LocalBackend(BaseBackend):
    """Local backend."""

    def __init__(self, path: str):
        """Local backend.

        Args:
            path: folder where trail data will be saved.
        """
        self.path = path

    def save_trial(self, trial):
        """Saves given trial.

        Args:
            trial: trial to save
        """
        return self.path
