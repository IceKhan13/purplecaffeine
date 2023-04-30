"""Tests for Backend."""
import os
from unittest import TestCase

from purplecaffeine.trial import Trial
from purplecaffeine.backend import LocalBackend

from .common import test_teardown


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
        self.local_backend.save_trial(name=self.temp, trial=self.my_trial)
        self.assertTrue(
            os.path.isfile(os.path.join(self.res_path, self.temp + ".json"))
        )

    def test_read_backend(self):
        """Test read trial."""
        trial_json = self.local_backend.read_trial(name=self.my_trial.name)
        self.assertTrue(isinstance(trial_json, object))

    def tearDown(self) -> None:
        """TearDown Backend object."""
        test_teardown(self)
