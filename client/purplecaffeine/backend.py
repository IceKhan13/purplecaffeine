"""Backend."""
import os
import json

from purplecaffeine.utils import TrialEncoder, TrialDecoder


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
            json.dump(trial_file, trial, cls=TrialEncoder)

        return self.path

    def read_trial(self, name: str) -> dict:
        """Read a given trial file.

        Args:
            name: name of the trial

        Returns:
            trial: object of a trial
        """
        with open(
            os.path.join(self.path, name + ".json"), "r", encoding="utf-8"
        ) as trial_file:
            return json.load(trial_file, cls=TrialDecoder)
