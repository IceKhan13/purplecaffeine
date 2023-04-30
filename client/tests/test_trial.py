"""Tests for Trial."""
import os
from unittest import TestCase
from qiskit.providers import Backend

from purplecaffeine.trial import Trial

from .common import populate_trial, test_setup, test_teardown


class TestTrial(TestCase):  # pylint: disable=no-member
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        test_setup(test_obj=self)

    def populate_trial(self, trial: Trial):
        """Populate Trial with data."""
        populate_trial(test_obj=self, trial=trial)

    def test_trial_context(self):
        """Test train context."""
        with Trial(name=self.temp, backend=self.local_backend) as trial:
            trial.add_metric(self.metric_name, self.metric)
        trial.read_trial()
        self.assertTrue(
            os.path.isfile(os.path.join(self.res_path, trial.name + ".json"))
        )
        self.assertEqual(trial.metrics, [(self.metric_name, self.metric)])

    def test_add_trial(self):
        """Test adding stuff into Trial."""
        # Add everything
        self.populate_trial(self.my_trial)
        # Check everything
        self.assertEqual(self.my_trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(self.my_trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(self.my_trial.circuits, [(self.circ_name, self.circ)])
        self.assertEqual(self.my_trial.qbackends, [(self.backend_name, self.backend)])
        self.assertEqual(self.my_trial.operators, [(self.ope_name, self.ope)])
        self.assertEqual(self.my_trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(self.my_trial.texts, [(self.title, self.text)])
        self.assertEqual(self.my_trial.arrays, [(self.array_name, self.array)])
        self.assertEqual(self.my_trial.tags, self.my_tags)

    def test_save_and_read(self):
        """Test save and read Trial."""
        temp_trial = Trial(name=self.temp, backend=self.local_backend)
        # Populate Trial data
        self.populate_trial(temp_trial)
        # Save Trial into localbackend
        temp_trial.save_trial()
        self.assertTrue(
            os.path.isfile(os.path.join(self.res_path, temp_trial.name + ".json"))
        )
        # Read Trial from localbackend
        temp_trial.read_trial()
        self.assertEqual(temp_trial.name, self.temp)
        self.assertEqual(temp_trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(temp_trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(temp_trial.circuits, [(self.circ_name, self.circ)])
        self.assertEqual(
            str(temp_trial.qbackends), str([(self.backend_name, self.backend)])
        )
        self.assertTrue(isinstance(temp_trial.qbackends[0][1], Backend))
        self.assertEqual(temp_trial.operators, [(self.ope_name, self.ope)])
        self.assertEqual(temp_trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(temp_trial.texts, [(self.title, self.text)])
        self.assertEqual(str(temp_trial.arrays), str([(self.array_name, self.array)]))
        self.assertEqual(temp_trial.tags, self.my_tags)

    def tearDown(self) -> None:
        """TearDown Trial object."""
        self.artifact.close()
        test_teardown(self)
