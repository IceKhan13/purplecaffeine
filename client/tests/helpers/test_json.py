"""Tests for Json."""
import os
from unittest import TestCase
from qiskit_aer import AerSimulator
from qiskit.providers import Backend
from qiskit import execute, QuantumCircuit
from qiskit.extensions import XGate
from qiskit.quantum_info.operators import Operator

from purplecaffeine.trial import Trial
from purplecaffeine.backend import LocalBackend
from purplecaffeine.helpers import Encoder, Decoder


class TestJson(TestCase):
    """TestJson."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.res_path = os.path.join(current_directory, "../resources")
        self.local_backend = LocalBackend(path=self.res_path)
        self.my_trial = Trial(name="keep_trial")
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
        self.artifact = self.res_path + "/qiskit.png"

        # Description
        self.title = "description"
        self.text = "This is my very much awesome experiment !"
        self.my_tags = ["quantum", "test"]

    def populate_trial(self):
        """Populate Trial with data."""
        self.my_trial.add_metric(self.metric_name, self.metric)
        self.my_trial.add_parameter(self.param_name, self.param)
        self.my_trial.add_circuit(self.circ_name, self.circ)
        self.my_trial.add_qbackend(self.backend_name, self.backend)
        self.my_trial.add_operator(self.ope_name, self.ope)
        self.my_trial.add_artifact(self.artifact_name, self.artifact)
        self.my_trial.add_text(self.title, self.text)
        self.my_trial.add_array(self.array_name, self.array)
        for tags in self.my_tags:
            self.my_trial.add_tag(tags)

    def _encoder(self):
        """Test encoder data."""
        self.populate_trial()
        Encoder(self.my_trial)

    def _decoder(self):
        """Test decoder data."""
        trial_json = self.local_backend.read_trial(name=self.my_trial.name)
        trial_decode = Decoder(payload=trial_json)
        self.assertTrue(isinstance(trial_decode.name, str))
        self.assertTrue(isinstance(trial_decode.metrics, list))
        self.assertTrue(isinstance(trial_decode.parameters, list))
        self.assertTrue(isinstance(trial_decode.circuits[0][1], QuantumCircuit))
        # self.assertTrue(isinstance(trial_decode.qbackends[0][1], Backend))
        self.assertTrue(isinstance(trial_decode.operators[0][1], Operator))
        # self.assertTrue(isinstance(trial_decode.artifacts, list))
        self.assertTrue(isinstance(trial_decode.texts[0][1], str))
        self.assertTrue(isinstance(trial_decode.arrays, list))
        self.assertTrue(isinstance(trial_decode.tags, list))
