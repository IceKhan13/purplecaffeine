"""Tests for Json."""
import json
import copy
from unittest import TestCase

from qiskit_ibm_runtime.utils import RuntimeEncoder

from purplecaffeine.core import Trial
from purplecaffeine.utils import TrialEncoder, TrialDecoder

from ..test_trial import dummy_trial


class TestJson(TestCase):
    """TestJson."""

    def test_encoder_decoder(self):
        """Test encoder / decoder."""
        my_trial = dummy_trial(name="keep_trial")
        # Encoder
        trial_encode = json.dumps(my_trial.__dict__, cls=TrialEncoder, indent=4)
        self.assertTrue(isinstance(trial_encode, str))
        for circuit in my_trial.circuits:
            circ_encode = json.dumps(circuit, cls=RuntimeEncoder, indent=4)
        for text in my_trial.texts:
            text_encode = json.dumps(text, cls=RuntimeEncoder, indent=4)

        # Decoder
        trial_decode = Trial(**json.loads(trial_encode, cls=TrialDecoder))
        for index, circuit in enumerate(copy.copy(trial_decode.circuits)):
            trial_decode.circuits[index] = json.loads(circ_encode, cls=TrialDecoder)
        for index, text in enumerate(copy.copy(trial_decode.texts)):
            trial_decode.texts[index] = json.loads(text_encode, cls=TrialDecoder)

        self.assertTrue(isinstance(trial_decode, Trial))
        self.assertEqual(trial_decode.metrics, my_trial.metrics)
        self.assertEqual(trial_decode.parameters, my_trial.parameters)
        self.assertEqual(trial_decode.circuits, my_trial.circuits)
        self.assertEqual(trial_decode.operators, my_trial.operators)
        self.assertEqual(trial_decode.texts, my_trial.texts)
        self.assertEqual(trial_decode.arrays, my_trial.arrays)
        self.assertEqual(trial_decode.tags, my_trial.tags)
