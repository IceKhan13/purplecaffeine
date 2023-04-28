"""Tests for Backend."""
import os
import json
from unittest import TestCase
from purplecaffeine.trial import Trial
from purplecaffeine.backend import LocalBackend


class TestBackend(TestCase):
    """TestBackend."""

    def setUp(self) -> None:
        """SetUp Backend object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.res_path = os.path.join(current_directory, "resources")

        # Setting up local backend
        self.temp = "to_remove"
        self.local_backend = LocalBackend(path=self.res_path)
        self.my_trial = Trial(name="keep_trial", backend=self.local_backend)
        self.my_trial.add_metric("some-metrics", 2)

    def test_save_backend(self):
        """Test save trial."""
        to_register = {
            "name": f"{self.my_trial.name}",
            "metrics": f"{self.my_trial.metrics}",
        }
        trial_json = json.dumps(to_register)

        self.local_backend.save_trial(name=self.temp, trial_json=trial_json)
        self.assertTrue(os.path.isfile(self.res_path + "/" + self.temp + ".json"))

    def test_read_backend(self):
        """Test read trial."""
        trial_json = self.local_backend.read_trial(name=self.my_trial.name)
        self.assertTrue(isinstance(trial_json, dict))

    def tearDown(self) -> None:
        """TearDown Backend object."""
        file_to_remove = self.res_path + "/" + self.temp + ".json"
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)
