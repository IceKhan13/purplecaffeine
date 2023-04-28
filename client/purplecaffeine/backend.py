"""Backend."""
import json


class BaseBackend:
    """Base backend class."""

    def save_trial(self, name: str, trial_json: json):
        """Saves given trial.

        Args:
            name: name of the trial
            trial_json: encode trial to save
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

    def save_trial(self, name: str, trial_json: json) -> str:
        """Saves given trial.

        Args:
            name: name of the trial
            trial_json: encode trial to save

        Returns:
            self.path: path of the trial file
        """

        with open(self.path + "/" + name + ".json", "w") as trial_file:
            trial_file.write(trial_json)

        return self.path

    def read_trial(self, name) -> dict:
        """Read a given trial file.

        Args:
            name: name of the trial

        Returns:
            trial_json: Json object of a trial
        """
        with open(self.path + "/" + name + ".json", "r") as trial_file:
            trial_json = json.loads(trial_file.read())

        return trial_json
