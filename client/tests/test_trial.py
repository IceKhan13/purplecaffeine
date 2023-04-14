"""Tests for Trial."""
import os
from unittest import TestCase
from qiskit_aer import AerSimulator
from qiskit import execute, QuantumCircuit
from qiskit.extensions import XGate
from qiskit.quantum_info.operators import Operator

from purplecaffeine.trial import Trial


class TestTrial(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        res_path = os.path.join(current_directory, "resources")
        self.my_trial = Trial("My Awesome Trial !")
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
        job = execute(self.circ, self.backend, shots=512, memory=True)
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
