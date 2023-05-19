"""Tests for Backend."""
import os
import shutil
from pathlib import Path
from unittest import TestCase, skip

from purplecaffeine.core import Trial, LocalBackend, ApiBackend
from .test_trial import dummy_trial


class TestBackend(TestCase):
    """TestBackend."""

    def setUp(self) -> None:
        """SetUp Backend object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(current_directory, "test_backend")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_backend = LocalBackend(path=self.save_path)
        self.my_trial = dummy_trial(name="keep_trial", backend=self.local_backend)

    def test_save_get_list_local_backend(self):
        """Test save trial locally."""
        # Save
        self.local_backend.save(trial=self.my_trial)
        self.assertTrue(
            os.path.isfile(os.path.join(self.save_path, f"{self.my_trial.uuid}.json"))
        )
        # Get
        recovered = self.local_backend.get(trial_id=self.my_trial.uuid)
        self.assertTrue(isinstance(recovered, Trial))
        self.assertEqual(recovered.parameters, [["test_parameter", "parameter"]])
        with self.assertRaises(ValueError):
            self.local_backend.get(trial_id="999")
        # List
        list_trials = self.local_backend.list()
        self.assertTrue(isinstance(list_trials, list))
        self.assertTrue(isinstance(list_trials[0], Trial))

    @skip("Remote call.")
    def test_save_get_api_backend(self):
        """Test save trial remotely."""
        # Save
        backend = ApiBackend(host="", username="", password="")
        backend.save(trial=self.my_trial)
        # Get
        recovered = backend.get(trial_id="1")
        self.assertTrue(isinstance(recovered, Trial))
        self.assertEqual(recovered.parameters, [["test_parameter", "parameter"]])
        with self.assertRaises(ValueError):
            backend.get(trial_id="999")

    def tearDown(self) -> None:
        """TearDown Backend object."""
        file_to_remove = os.path.join(self.save_path)
        if os.path.exists(file_to_remove):
            shutil.rmtree(file_to_remove)
