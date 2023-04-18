"""Tests for Backend."""
import os
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
        self.local_backend = LocalBackend(path=self.res_path)
        with Trial(name="test_backend", backend=self.local_backend) as self.my_trial:
            self.my_trial.add_metric("some-metrics", 2)

    def test_save_trial(self):
        """Test save trial."""
        self.local_backend.save_trial(self.my_trial)
        self.assertTrue(
            os.path.isfile(self.res_path + "/" + self.my_trial.name + ".json")
        )

    def test_read_trial(self):
        """Test read trial."""
        trial_json = self.local_backend.read_trial(name=self.my_trial.name)
        self.assertTrue(isinstance(trial_json, dict))

    def tearDown(self) -> None:
        """TearDown Backend object."""
        os.remove(self.res_path + "/" + self.my_trial.name + ".json")
