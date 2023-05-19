"""Tests for Trial."""
import os
import shutil
from pathlib import Path
from typing import Optional
from unittest import TestCase, skip

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate
from qiskit.quantum_info import Operator

from purplecaffeine import Trial, LocalBackend, ApiBackend, BaseBackend as TrialBackend


def dummy_trial(
    name: Optional[str] = "test_trial", backend: Optional[TrialBackend] = None
):
    """Returns dummy trial for tests.

    Returns:
        dummy trial
    """
    trial = Trial(name=name, backend=backend)
    trial.add_metric("test_metric", 42)
    trial.add_parameter("test_parameter", "parameter")
    trial.add_circuit("test_circuit", QuantumCircuit(2))
    trial.add_operator("test_operator", Operator(XGate()))
    trial.add_text("test_text", "text")
    trial.add_array("test_array", np.array([42]))
    trial.add_tag("qiskit")
    trial.add_tag("test")
    return trial


class TestTrial(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(current_directory, "resources")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_backend = LocalBackend(path=self.save_path)

    def test_trial_context(self):
        """Test train context."""
        uuid = "some_uuid"
        with Trial(name="test_trial", backend=self.local_backend, uuid=uuid) as trial:
            trial.add_metric("test_metric", 42)
        trial.read(trial_id=uuid)
        self.assertTrue(os.path.isfile(os.path.join(self.save_path, f"{uuid}.json")))
        self.assertEqual(trial.metrics, [["test_metric", 42]])

    def test_add_trial(self):
        """Test adding stuff into Trial."""
        trial = dummy_trial()

        self.assertEqual(trial.metrics, [["test_metric", 42]])
        self.assertEqual(trial.parameters, [["test_parameter", "parameter"]])
        self.assertEqual(trial.circuits, [["test_circuit", QuantumCircuit(2)]])
        self.assertEqual(trial.operators, [["test_operator", Operator(XGate())]])
        self.assertEqual(trial.texts, [["test_text", "text"]])
        self.assertEqual(trial.arrays, [["test_array", np.array([42])]])
        self.assertEqual(trial.tags, ["qiskit", "test"])

    def test_save_read_local_trial(self):
        """Test save and read Trial locally."""
        trial = dummy_trial(backend=self.local_backend)
        trial.save()

        self.assertTrue(
            os.path.isfile(os.path.join(self.save_path, f"{trial.uuid}.json"))
        )
        recovered = trial.read(trial_id=trial.uuid)
        self.assertEqual(recovered.metrics, [["test_metric", 42]])
        self.assertEqual(recovered.parameters, [["test_parameter", "parameter"]])
        self.assertEqual(recovered.circuits, [["test_circuit", QuantumCircuit(2)]])
        self.assertEqual(recovered.operators, [["test_operator", Operator(XGate())]])
        self.assertEqual(recovered.texts, [["test_text", "text"]])
        self.assertEqual(recovered.arrays, [["test_array", np.array([42])]])
        self.assertEqual(recovered.tags, ["qiskit", "test"])

    @skip("Remote call")
    def test_save_read_api_trial(self):
        """Test save and read Trial remotely."""
        backend = ApiBackend(username="", password="", host="")
        trial = dummy_trial(backend=backend)
        trial.save()

        recovered = trial.read(trial_id="1")
        self.assertEqual(recovered.metrics, [["test_metric", 42]])
        self.assertEqual(recovered.parameters, [["test_parameter", "parameter"]])
        self.assertEqual(recovered.circuits, [["test_circuit", QuantumCircuit(2)]])
        self.assertEqual(recovered.operators, [["test_operator", Operator(XGate())]])
        self.assertEqual(recovered.texts, [["test_text", "text"]])
        self.assertEqual(recovered.arrays, [["test_array", np.array([42])]])
        self.assertEqual(recovered.tags, ["qiskit", "test"])

    def test_export_import(self):
        """Test export and import Trial from shared file."""
        trial = dummy_trial()
        # Export
        trial.export_to_shared_file(path=self.save_path)
        self.assertTrue(
            os.path.isfile(os.path.join(self.save_path, f"{trial.uuid}.json"))
        )
        # Import
        new_trial = Trial("test_import").import_from_shared_file(
            os.path.join(self.save_path, f"{trial.uuid}.json")
        )
        self.assertEqual(new_trial.metrics, [["test_metric", 42]])
        self.assertEqual(new_trial.parameters, [["test_parameter", "parameter"]])
        self.assertEqual(new_trial.circuits, [["test_circuit", QuantumCircuit(2)]])
        self.assertEqual(new_trial.operators, [["test_operator", Operator(XGate())]])
        self.assertEqual(new_trial.texts, [["test_text", "text"]])
        self.assertEqual(new_trial.arrays, [["test_array", np.array([42])]])
        self.assertEqual(new_trial.tags, ["qiskit", "test"])

    def tearDown(self) -> None:
        """TearDown Trial object."""
        file_to_remove = os.path.join(self.save_path)
        if os.path.exists(file_to_remove):
            shutil.rmtree(file_to_remove)
