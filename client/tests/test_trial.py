"""Tests for Trial."""
import os
from unittest import TestCase
from PIL import Image
from qiskit_aer import AerSimulator
from qiskit.providers import Backend
from qiskit import execute, QuantumCircuit
from qiskit.extensions import XGate
from qiskit.quantum_info.operators import Operator

from purplecaffeine.trial import Trial
from purplecaffeine.backend import LocalBackend


class TestTrial(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        self.temp = "to_remove"
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
        job = execute(self.circ, self.backend, shots=1, memory=False)
        self.array_name = "result"
        self.array = job.result()

        # Imaginary artifact
        self.artifact_name = "Qiskit logo"
        self.artifact = Image.open(self.res_path + "/qiskit.png")

        # Description
        self.title = "description"
        self.text = "This is my very much awesome experiment !"
        self.my_tags = ["quantum", "test"]

    def populate_trial(self, trial: Trial):
        """Populate Trial with data."""
        trial.add_metric(self.metric_name, self.metric)
        trial.add_parameter(self.param_name, self.param)
        trial.add_circuit(self.circ_name, self.circ)
        trial.add_qbackend(self.backend_name, self.backend)
        trial.add_operator(self.ope_name, self.ope)
        trial.add_artifact(self.artifact_name, self.artifact)
        trial.add_text(self.title, self.text)
        trial.add_array(self.array_name, self.array)
        for tags in self.my_tags:
            trial.add_tag(tags)

    def test_trial_context(self):
        """Test train context."""
        with Trial(name=self.temp, backend=self.local_backend) as trial:
            trial.add_metric(self.metric_name, self.metric)
        trial.read_trial()
        self.assertTrue(os.path.isfile(self.res_path + "/" + trial.name + ".json"))
        self.assertEqual(trial.metrics, [(self.metric_name, self.metric)])

    def test_add_trial(self):
        """Test adding stuff into Trial."""
        # Add everything
        self.populate_trial(self.my_trial)
        # Check everything
        self.assertEqual(self.my_trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(self.my_trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(self.my_trial.circuits, [(self.circ_name, self.circ)])
        self.assertEqual(self.my_trial.qbackends, [(self.backend_name, self.backend)])
        self.assertEqual(self.my_trial.operators, [(self.ope_name, self.ope)])
        self.assertEqual(self.my_trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(self.my_trial.texts, [(self.title, self.text)])
        self.assertEqual(self.my_trial.arrays, [(self.array_name, self.array)])
        self.assertEqual(self.my_trial.tags, self.my_tags)

    def test_save_and_read(self):
        """Test save and read Trial."""
        temp_trial = Trial(name=self.temp, backend=self.local_backend)
        # Populate Trial data
        self.populate_trial(temp_trial)
        # Save Trial into localbackend
        temp_trial.save_trial()
        self.assertTrue(os.path.isfile(self.res_path + "/" + temp_trial.name + ".json"))
        # Read Trial from localbackend
        temp_trial.read_trial()
        self.assertEqual(temp_trial.name, self.temp)
        self.assertEqual(temp_trial.metrics, [(self.metric_name, self.metric)])
        self.assertEqual(temp_trial.parameters, [(self.param_name, self.param)])
        self.assertEqual(temp_trial.circuits, [(self.circ_name, self.circ)])
        self.assertEqual(
            str(temp_trial.qbackends), str([(self.backend_name, self.backend)])
        )
        self.assertTrue(isinstance(temp_trial.qbackends[0][1], Backend))
        self.assertEqual(temp_trial.operators, [(self.ope_name, self.ope)])
        self.assertEqual(temp_trial.artifacts, [(self.artifact_name, self.artifact)])
        self.assertEqual(temp_trial.texts, [(self.title, self.text)])
        self.assertEqual(str(temp_trial.arrays), str([(self.array_name, self.array)]))
        self.assertEqual(temp_trial.tags, self.my_tags)

    def tearDown(self) -> None:
        """TearDown Trial object."""
        self.artifact.close()
        file_to_remove = self.res_path + "/" + self.temp + ".json"
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)
