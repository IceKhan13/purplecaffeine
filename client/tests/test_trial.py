"""Tests for Trial."""
from unittest import TestCase
import os
from qiskit import execute, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.extensions import XGate
from qiskit.quantum_info.operators import Operator

from purplecaffeine.trial import Trial


class TestTrial(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        res_path = "{}/resources".format(current_directory)
        self.my_trial = Trial("My Awesome Trial !")
        nb_qubit = 2

        # Create metric
        self.metric_name = "nb_qubit"
        self.metric = nb_qubit

        # Create custom parameters
        self.param_name = "OS"
        self.param = "Ubuntu"

        # Create custom operators
        self.op_name = "XGate"
        self.op = Operator(XGate())

        # Create the circuit
        self.qc_name = "Custom circuit"
        self.qc = QuantumCircuit(nb_qubit)
        self.qc.append(self.op, [1])
        self.qc.cx(1, 0)
        self.qc.measure_all()

        # Run circuit
        self.backend_name = "AerSimulator"
        self.backend = AerSimulator()
        job = execute(self.qc, self.backend, shots=512, memory=True)
        self.array = job.result()

        # Imaginary artifact
        self.artifact_name = "Qiskit logo"
        self.artifact = res_path + "/qiskit.png"

        # Description
        self.title = "description"
        self.text = "This is my very much awesome experiment !"

    def test_trail_context(self):
        """Test train context."""
        with Trial("test_trial") as trial:
            trial.add_metric(self.metric_name, self.metric)
        self.assertEqual(trial.metrics, [(self.metric_name, self.metric)])

    def test_trail_add(self):
        """Test adding stuff into Trial."""
        # Add everything
        self.my_trial.add_metric(self.metric_name, self.metric)
        self.my_trial.add_parameter(self.param_name, self.param)
        self.my_trial.add_circuit(self.qc_name, self.qc)
        self.my_trial.add_qbackend(self.backend_name, self.backend)
        self.my_trial.add_operator(self.op_name, self.op)
        self.my_trial.add_artifact(self.artifact_name, self.artifact)
        self.my_trial.add_text(self.title, self.text)
        self.my_trial.add_array(self.array)
        # Check everything
        self.assertEqual(self.my_trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(self.my_trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(self.my_trial.circuits, [(self.qc_name, self.qc)])
        self.assertEqual(self.my_trial.qbackends, [(self.backend_name, self.backend)])
        self.assertEqual(self.my_trial.operators, [(self.op_name, self.op)])
        self.assertEqual(self.my_trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(self.my_trial.texts, [(self.title, self.text)])
        self.assertEqual(self.my_trial.arrays, [self.array])
