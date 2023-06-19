"""Tests for Widget."""
import os
import shutil
from pathlib import Path
from unittest import TestCase

from ipywidgets import widgets
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

    def test_render_pagination(self):
        """Test to check that pagination buttons work correctly"""
        self.add_n_trials(20)
        widget = Widget(self.local_storage)
        box = widget.render_pagination()
        previous_button = box.children[0]
        next_button = box.children[1]
        self.assertFalse(next_button.disabled)
        self.assertTrue(previous_button.disabled)

    def test_render_trial(self):
        """Test to check that trails buttons are being displayed"""
        self.add_n_trials(5)
        widget = Widget(self.local_storage)
        tabs = widget.render_trial()
        info = tabs.children[0]
        self.assertTrue(self.local_storage.list()[0].uuid in info.value)

    def test_search(self):
        """Test to check the search function"""
        self.add_n_trials(20)
        widget = Widget(self.local_storage)
        box = widget.search()
        search_button = box.children[0]
        input_text = box.children[1]
        input_text.value = self.local_storage.list()[0].name
        search_button.click()
        self.assertEqual(widget.search_value, self.local_storage.list()[0].name)
        self.assertEqual(len(widget.trials), 1)
        input_text.value = ""
        search_button.click()
        self.assertEqual(len(widget.trials), 10)

    def test_load_detail(self):
        """Test to check that the selected trial is the first one"""
        self.add_n_trials(2)
        widget = Widget(self.local_storage)
        first_trail = self.local_storage.list()[0]
        button = widgets.Button(
            description=first_trail.name,
            disabled=False,
            button_style="",
            tooltip=first_trail.uuid,
            icon="",
        )
        widget.load_detail(button)
        self.assertEqual(widget.selected_trial.uuid, first_trail.uuid)

    def test_trial_list(self):
        """Test to check that new trials are being added."""
        self.add_n_trials(20)
        widget = Widget(self.local_storage)
        self.assertEqual(
            widget.render_trails_list().children[0].tooltip,
            self.local_storage.list()[0].uuid,
        )
        self.assertEqual(
            widget.render_trails_list().children[0].tooltip, widget.selected_trial.uuid
        )

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
                exp_value = (
                    Estimator().run(circuit, obs, shots=shots).result().values.item()
                )

                # track results of run
                trial.add_metric("exp_value", exp_value)

    def tearDown(self) -> None:
        """TearDown the trials objects."""
        trials_files = os.path.join(self.save_path)
        if os.path.exists(trials_files):
            shutil.rmtree(trials_files)
