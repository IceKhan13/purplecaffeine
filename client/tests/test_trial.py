"""Tests for Trial."""
import os
import shutil
from pathlib import Path
from typing import Optional
from unittest import TestCase

import numpy as np
from qiskit import QuantumCircuit, __qiskit_version__
from qiskit.circuit.library import XGate
from qiskit.quantum_info import Operator

from purplecaffeine import Trial, LocalStorage, BaseStorage as TrialStorage


def dummy_trial(
    name: Optional[str] = "test_trial", storage: Optional[TrialStorage] = None
):
    """Returns dummy trial for tests.

    Returns:
        dummy trial
    """
    trial = Trial(name=name, storage=storage)
    trial.add_description("Short desc")
    trial.add_metric("test_metric", 42)
    trial.add_parameter("test_parameter", "parameter")
    trial.add_circuit("test_circuit", QuantumCircuit(2))
    trial.add_operator("test_operator", Operator(XGate()))
    trial.add_text("test_text", "text")
    trial.add_array("test_array", np.array([42]))
    trial.add_tag("qiskit")
    trial.add_tag("test")
    trial.add_version("numpy", "1.2.3-4")
    return trial


class TestTrial(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(current_directory, "resources")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_storage = LocalStorage(path=self.save_path)

    def test_trial_context(self):
        """Test train context."""
        uuid = "some_uuid"
        with Trial(name="test_trial", storage=self.local_storage, uuid=uuid) as trial:
            trial.add_metric("test_metric", 42)
        trial.read(trial_id=uuid)
        self.assertTrue(os.path.isfile(os.path.join(self.save_path, f"{uuid}.json")))
        self.assertEqual(trial.metrics, [["test_metric", 42]])
        self.assertEqual(
            trial.versions, [[key, value] for key, value in __qiskit_version__.items()]
        )

    def test_add_trial(self):
        """Test adding stuff into Trial."""
        trial = dummy_trial()

        self.assertEqual(trial.description, "Short desc")
        self.assertEqual(trial.metrics, [["test_metric", 42]])
        self.assertEqual(trial.parameters, [["test_parameter", "parameter"]])
        self.assertEqual(trial.circuits, [["test_circuit", QuantumCircuit(2)]])
        self.assertEqual(trial.operators, [["test_operator", Operator(XGate())]])
        self.assertEqual(trial.texts, [["test_text", "text"]])
        self.assertEqual(trial.arrays, [["test_array", np.array([42])]])
        self.assertEqual(trial.tags, ["qiskit", "test"])
        self.assertEqual(trial.versions, [["numpy", "1.2.3-4"]])

    def test_save_read_local_trial(self):
        """Test save and read Trial locally."""
        trial = dummy_trial(storage=self.local_storage)
        trial.save()

        self.assertTrue(
            os.path.isfile(os.path.join(self.save_path, f"{trial.uuid}.json"))
        )
        recovered = trial.read(trial_id=trial.uuid)
        self.assertEqual(recovered.description, "Short desc")
        self.assertEqual(recovered.metrics, [["test_metric", 42]])
        self.assertEqual(recovered.parameters, [["test_parameter", "parameter"]])
        self.assertEqual(recovered.circuits, [["test_circuit", QuantumCircuit(2)]])
        self.assertEqual(recovered.operators, [["test_operator", Operator(XGate())]])
        self.assertEqual(recovered.texts, [["test_text", "text"]])
        self.assertEqual(recovered.arrays, [["test_array", np.array([42])]])
        self.assertEqual(recovered.tags, ["qiskit", "test"])
        self.assertEqual(recovered.versions, [["numpy", "1.2.3-4"]])

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
        self.assertEqual(new_trial.description, "Short desc")
        self.assertEqual(new_trial.metrics, [["test_metric", 42]])
        self.assertEqual(new_trial.parameters, [["test_parameter", "parameter"]])
        self.assertEqual(new_trial.circuits, [["test_circuit", QuantumCircuit(2)]])
        self.assertEqual(new_trial.operators, [["test_operator", Operator(XGate())]])
        self.assertEqual(new_trial.texts, [["test_text", "text"]])
        self.assertEqual(new_trial.arrays, [["test_array", np.array([42])]])
        self.assertEqual(new_trial.tags, ["qiskit", "test"])
        self.assertEqual(new_trial.versions, [["numpy", "1.2.3-4"]])

    def tearDown(self) -> None:
        """TearDown Trial object."""
        file_to_remove = os.path.join(self.save_path)
        if os.path.exists(file_to_remove):
            shutil.rmtree(file_to_remove)
