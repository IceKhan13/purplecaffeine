"""Tests for Backend."""
import os
import shutil
from pathlib import Path
from unittest import TestCase

from purplecaffeine.core import Trial, LocalBackend


class TestBackend(TestCase):
    """TestBackend."""

    def setUp(self) -> None:
        """SetUp Backend object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(current_directory, "test_backend")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_backend = LocalBackend(path=self.save_path)
        self.my_trial = Trial(name="keep_trial", backend=self.local_backend)
        self.my_trial.add_metric("some-metrics", 2)

    def test_save_and_load_backend(self):
        """Test save trial."""
        self.local_backend.save(trial=self.my_trial)
        self.assertTrue(os.path.isfile(os.path.join(self.save_path, "keep_trial.json")))
        recovered = self.local_backend.get(name="keep_trial")
        self.assertTrue(isinstance(recovered, Trial))
        self.assertEqual(recovered.parameters, [])

    def tearDown(self) -> None:
        """TearDown Backend object."""
        file_to_remove = os.path.join(self.save_path)
        if os.path.exists(file_to_remove):
            shutil.rmtree(file_to_remove)
