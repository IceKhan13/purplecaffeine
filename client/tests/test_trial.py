"""Tests for Trial."""
import os
from unittest import TestCase
from qiskit_aer import AerSimulator
from qiskit import execute, QuantumCircuit
from qiskit.extensions import XGate
from qiskit.quantum_info.operators import Operator

from purplecaffeine.trial import Trial
from purplecaffeine.backend import LocalBackend


class TestTrial(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.res_path = os.path.join(current_directory, "resources")
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
        job = execute(self.circ, self.backend, shots=512)
        self.array = job.result()

        # Imaginary artifact
        self.artifact_name = "Qiskit logo"
        self.artifact = self.res_path + "/qiskit.png"

        # Description
        self.title = "description"
        self.text = "This is my very much awesome experiment !"

    def test_trial_context(self):
        """Test train context."""
        with Trial(name="test_trial", backend=self.local_backend) as trial:
            trial.add_metric(self.metric_name, self.metric)
        self.assertEqual(trial.metrics, [(self.metric_name, self.metric)])

        trial.save_trial()
        self.assertTrue(
            os.path.isfile(self.res_path + "/" + trial.name + ".json")
        )
        trial.read_trial()

        os.remove(self.res_path + "/" + trial.name + ".json")

    def test_add_trial(self):
        """Test adding stuff into Trial."""
        # Add everything
        self.my_trial.add_metric(self.metric_name, self.metric)
        self.my_trial.add_parameter(self.param_name, self.param)
        self.my_trial.add_circuit(self.circ_name, self.circ)
        self.my_trial.add_qbackend(self.backend_name, self.backend)
        self.my_trial.add_operator(self.ope_name, self.ope)
        self.my_trial.add_artifact(self.artifact_name, self.artifact)
        self.my_trial.add_text(self.title, self.text)
        self.my_trial.add_array(self.array)
        # Check everything
        self.assertEqual(self.my_trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(self.my_trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(self.my_trial.circuits, [(self.circ_name, self.circ)])
        self.assertEqual(self.my_trial.qbackends, [(self.backend_name, self.backend)])
        self.assertEqual(self.my_trial.operators, [(self.ope_name, self.ope)])
        self.assertEqual(self.my_trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(self.my_trial.texts, [(self.title, self.text)])
        self.assertEqual(self.my_trial.arrays, [self.array])
        self.my_trial.save_trial()

    def test_read_trial(self):
        """Test read trial from Backend."""
        local_trial = Trial(name=self.my_trial.name, backend=self.local_backend)
        local_trial.read_trial()
        self.assertEqual(local_trial.name, self.my_trial.name)
        self.assertEqual(local_trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(local_trial.parameters, [(self.param_name, self.param)])
        # self.assertEqual(self.my_trial.circuits, [(self.circ_name, self.circ)])
        # self.assertEqual(self.my_trial.qbackends, [(self.backend_name, self.backend)])
        # self.assertEqual(self.my_trial.operators, [(self.ope_name, self.ope)])
        # self.assertEqual(self.my_trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(local_trial.texts, [(self.title, self.text)])
        # self.assertEqual(self.my_trial.arrays, [self.array])
