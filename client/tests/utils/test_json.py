"""Tests for Json."""
import json
from unittest import TestCase
from qiskit.providers import Backend

from purplecaffeine.trial import Trial
from purplecaffeine.utils import TrialEncoder, TrialDecoder

from ..common import populate_trial, test_setup


class TestJson(TestCase):  # pylint: disable=no-member
    """TestJson."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        test_setup(test_obj=self)

    def populate_trial(self, trial: Trial):
        """Populate Trial with data."""
        populate_trial(test_obj=self, trial=trial)

    def test_encoder_decoder(self):
        """Test encode and decode."""
        temp_trial = Trial(name="to_remove", backend=self.local_backend)
        # Populate Trial data
        self.populate_trial(temp_trial)
        # Encode
        encoded = json.dumps(temp_trial, cls=TrialEncoder)
        self.assertTrue(isinstance(json.loads(encoded), dict))

        # Decode
        trial = json.loads(encoded, cls=TrialDecoder)
        self.assertEqual(trial.name, self.temp)
        self.assertEqual(trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(trial.circuits, [(self.circ_name, self.circ)])
        self.assertEqual(str(trial.qbackends), str([(self.backend_name, self.backend)]))
        self.assertTrue(isinstance(trial.qbackends[0][1], Backend))
        self.assertEqual(trial.operators, [(self.ope_name, self.ope)])
        self.assertEqual(trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(trial.texts, [(self.title, self.text)])
        self.assertEqual(str(trial.arrays), str([(self.array_name, self.array)]))
        self.assertEqual(trial.tags, self.my_tags)

    def tearDown(self) -> None:
        """TearDown Trial object."""
        self.artifact.close()
