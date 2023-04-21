"""Backend."""
import json
from qiskit_ibm_runtime.utils import RuntimeEncoder, RuntimeDecoder


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
            path: folder where trial data will be saved.
        """
        self.path = path

    def save_trial(self, trial) -> str:
        """Saves given trial.

        Args:
            trial: trial to save

        Returns:
            self.path: path of the trial file
        """
        to_register = {
            "name": f"{trial.name}",
            "metrics": f"{trial.metrics}",
            "parameters": f"{trial.parameters}",
            "circuits": f"{trial.circuits}",
            "qbackends": f"{trial.qbackends}",
            "operators": f"{trial.operators}",
            "artifacts": f"{trial.artifacts}",
            "texts": f"{trial.texts}",
            "arrays": f"{trial.arrays}",
        }
        trial_json = json.dumps(to_register, cls=RuntimeEncoder)

        with open(self.path + "/" + trial.name + ".json", "w") as trial_file:
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
            trial_json = json.loads(trial_file.read(), cls=RuntimeDecoder)

        return trial_json
