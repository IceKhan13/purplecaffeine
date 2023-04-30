"""Tests for Json."""
import os
import json
from unittest import TestCase
from PIL import Image
from qiskit_aer import AerSimulator
from qiskit.providers import Backend
from qiskit import execute, QuantumCircuit
from qiskit.extensions import XGate
from qiskit.quantum_info.operators import Operator

from purplecaffeine.trial import Trial
from purplecaffeine.backend import LocalBackend
from purplecaffeine.utils import TrialEncoder, TrialDecoder


class TestJson(TestCase):
    """TestJson."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        self.temp = "to_remove"
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.res_path = os.path.join(current_directory, "../resources")
        self.local_backend = LocalBackend(path=self.res_path)
        self.my_trial = Trial(name="keep_trial", backend=self.local_backend)
        nb_qubit = 2

        # Create metric
        self.metric_name = "nb_qubit"
        self.metric = nb_qubit

        # Create custom parameters
        self.param_name = "OS"
        self.param = "Ubuntu"

        # Create custom operators
        self.ope_name = "XGate"
        self.ope = Operator(XGate())

        # Create the circuit
        self.circ_name = "Custom circuit"
        self.circ = QuantumCircuit(nb_qubit)
        self.circ.append(self.ope, [1])
        self.circ.cx(1, 0)
        self.circ.measure_all()

        # Run circuit
        self.backend_name = "AerSimulator"
        self.backend = AerSimulator()
        job = execute(self.circ, self.backend, shots=1, memory=False)
        self.array_name = "result"
        self.array = job.result()

        # Imaginary artifact
        self.artifact_name = "Qiskit logo"
        self.artifact = Image.open(os.path.join(self.res_path, "qiskit.png"))

        # Description
        self.title = "description"
        self.text = "This is my very much awesome experiment !"
        self.my_tags = ["quantum", "test"]

    def populate_trial(self, trial: Trial):
        """Populate Trial with data."""
        trial.add_metric(self.metric_name, self.metric)
        trial.add_metric("toto", 12)
        trial.add_parameter(self.param_name, self.param)
        trial.add_circuit(self.circ_name, self.circ)
        trial.add_qbackend(self.backend_name, self.backend)
        trial.add_operator(self.ope_name, self.ope)
        # trial.add_artifact(self.artifact_name, self.artifact)
        trial.add_text(self.title, self.text)
        trial.add_array(self.array_name, self.array)
        for tags in self.my_tags:
            trial.add_tag(tags)

    def test_encoder(self):
        """Test encoder"""
        temp_trial = Trial(name=self.temp, backend=self.local_backend)
        # Populate Trial data
        self.populate_trial(temp_trial)
        encoded = json.dumps(temp_trial, cls=TrialEncoder)
        self.assertTrue(isinstance(json.loads(encoded), dict))

    def test_decoder(self):
        """Test decoder"""
        temp_trial = Trial(name=self.temp, backend=self.local_backend)
        # Populate Trial data
        self.populate_trial(temp_trial)
        with open(
            os.path.join(self.local_backend.path, temp_trial.name + ".json"),
            "w",
            encoding="utf-8",
        ) as trial_file:
            trial_file.write(json.dumps(temp_trial, cls=TrialEncoder))

        with open(
            os.path.join(self.local_backend.path, temp_trial.name + ".json"),
            "r",
            encoding="utf-8",
        ) as trial_file:
            trial = json.loads(trial_file.read(), cls=TrialDecoder)

        self.assertEqual(trial.name, self.temp)
        self.assertEqual(trial.metrics, [(self.metric_name, self.metric), ("toto", 12)])
        self.assertEqual(trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(trial.circuits, [(self.circ_name, self.circ)])
        self.assertEqual(
            str(temp_trial.qbackends), str([(self.backend_name, self.backend)])
        )
        self.assertTrue(isinstance(trial.qbackends[0][1], Backend))
        self.assertEqual(trial.operators, [(self.ope_name, self.ope)])
        # self.assertEqual(trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(trial.texts, [(self.title, self.text)])
        self.assertEqual(str(trial.arrays), str([(self.array_name, self.array)]))
        self.assertEqual(trial.tags, self.my_tags)

    def tearDown(self) -> None:
        """TearDown Trial object."""
        self.artifact.close()
