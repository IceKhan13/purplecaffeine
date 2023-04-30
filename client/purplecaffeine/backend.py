"""Backend."""
import os
import json


class BaseBackend:
    """Base backend class."""

    def save_trial(self, name: str, trial):
        """Saves given trial.

        Args:
            name: name of the trial
            trial: encode trial to save
        """
        raise NotImplementedError


class LocalBackend(BaseBackend):
    """Local backend."""

    def __init__(self, path: str):
        """Local backend.

        Args:
            path: folder where trial data will be saved.
        """
        self.path = path

    def save_trial(self, name: str, trial) -> str:
        """Saves given trial.

        Args:
            name: name of the trial
            trial: encode trial to save

        Returns:
            self.path: path of the trial file
        """
        with open(
            os.path.join(self.path, name + ".json"), "w", encoding="utf-8"
        ) as trial_file:
            trial_file.write(trial)

        return self.path

    def read_trial(self, name) -> dict:
        """Read a given trial file.

        Args:
            name: name of the trial

        Returns:
            trial: Json object of a trial
        """
        with open(
            os.path.join(self.path, name + ".json"), "r", encoding="utf-8"
        ) as trial_file:
            trial = json.loads(trial_file.read())

        return trial
