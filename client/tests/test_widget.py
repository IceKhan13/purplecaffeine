"""Tests for Trial."""
import os
from pathlib import Path
from unittest import TestCase
from qiskit.circuit.random import random_circuit
from qiskit.primitives import Estimator
from qiskit.quantum_info.random import random_pauli

from purplecaffeine.core import LocalStorage, Trial
from purplecaffeine.widget import Widget


class TestWidget(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp local storage backend for widget use"""
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(curr_dir, "test")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_storage = LocalStorage(path=self.save_path)

    def test_trial_list(self):
        """Test to check that new trials are being added."""
        self.add_n_trials(20)
        widget = Widget(self.local_storage)
        self.assertEqual(widget.render_trails_list()
                         .children[0].tooltip,
                         self.local_storage.list()[0].uuid)
        self.assertEqual(widget.render_trails_list()
                         .children[0].tooltip,
                         widget.selected_trial.uuid)

    def add_n_trials(self, number_of_trials):
        """Aux function to add 20 trials to the class storage"""
        n_qubits = 4
        depth = 3
        shots = 2000

        circuit = random_circuit(n_qubits, depth)
        obs = random_pauli(n_qubits)
        for i in range(0, number_of_trials):
            with Trial("Example trial " + str(i), storage=self.local_storage) as trial:
                # track some parameters
                trial.add_parameter("estimator", "qiskit.primitives.Estimator")
                trial.add_parameter("depth", str(depth))
                trial.add_parameter("n_qubits", str(n_qubits))
                trial.add_parameter("shots", str(shots))

                # track objects of interest
                trial.add_circuit("circuit", circuit)

                # run
                exp_value = Estimator().run(circuit, obs, shots=shots).result().values.item()

                # track results of run
                trial.add_metric("exp_value", exp_value)

    def test_empty_string(self):
        """Test when we don't have trials."""
        widget = Widget(self.local_storage)
        self.assertEqual(widget.display_message("Add a new trial to see the info of that trial ")
                         .value,
                         "<h1 style='text-align: center;'> <br><br><br>Add a new trial "
                         "to see the "
                         "info of that trial </h1>"
                         '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/'
                         'bootstrap@5.2.3/dist/'
                         'css/bootstrap.min.css" '
                         'integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW'
                         '1RWuH61DGLwZJEdK2Kadq2F9CUG65" '
                         'crossorigin="anonymous">')
