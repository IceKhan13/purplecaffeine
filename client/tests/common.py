"""Common functions for tests."""
import os
from PIL import Image
from qiskit_aer import AerSimulator
from qiskit import execute, QuantumCircuit
from qiskit.extensions import XGate
from qiskit.quantum_info.operators import Operator

from purplecaffeine.trial import Trial
from purplecaffeine.backend import LocalBackend


def populate_trial(test_obj, trial: Trial):
    """Populate Trial with data."""
    trial.add_metric(test_obj.metric_name, test_obj.metric)
    trial.add_parameter(test_obj.param_name, test_obj.param)
    trial.add_circuit(test_obj.circ_name, test_obj.circ)
    trial.add_qbackend(test_obj.backend_name, test_obj.backend)
    trial.add_operator(test_obj.ope_name, test_obj.ope)
    trial.add_artifact(test_obj.artifact_name, test_obj.artifact)
    trial.add_text(test_obj.title, test_obj.text)
    trial.add_array(test_obj.array_name, test_obj.array)
    for tags in test_obj.my_tags:
        trial.add_tag(tags)


def test_setup(test_obj) -> None:
    """Standard SetUp function."""
    test_obj.temp = "to_remove"
    current_directory = os.path.dirname(os.path.abspath(__file__))
    test_obj.res_path = os.path.join(current_directory, "resources")
    test_obj.local_backend = LocalBackend(path=test_obj.res_path)
    test_obj.my_trial = Trial(name="keep_trial", backend=test_obj.local_backend)
    nb_qubit = 2

    # Create metric
    test_obj.metric_name = "nb_qubit"
    test_obj.metric = nb_qubit

    # Create custom parameters
    test_obj.param_name = "OS"
    test_obj.param = "Ubuntu"

    # Create custom operators
    test_obj.ope_name = "XGate"
    test_obj.ope = Operator(XGate())

    # Create the circuit
    test_obj.circ_name = "Custom circuit"
    test_obj.circ = QuantumCircuit(nb_qubit)
    test_obj.circ.append(test_obj.ope, [1])
    test_obj.circ.cx(1, 0)
    test_obj.circ.measure_all()

    # Run circuit
    test_obj.backend_name = "AerSimulator"
    test_obj.backend = AerSimulator()
    job = execute(test_obj.circ, test_obj.backend, shots=1, memory=False)
    test_obj.array_name = "result"
    test_obj.array = job.result()

    # Imaginary artifact
    test_obj.artifact_name = "Qiskit logo"
    test_obj.artifact = Image.open(os.path.join(test_obj.res_path, "qiskit.png"))

    # Description
    test_obj.title = "description"
    test_obj.text = "This is my very much awesome experiment !"
    test_obj.my_tags = ["quantum", "test"]
    return test_obj


def test_teardown(test_obj) -> None:
    """Standard TearDown function."""
    file_to_remove = os.path.join(test_obj.res_path, test_obj.temp + ".json")
    if os.path.exists(file_to_remove):
        os.remove(file_to_remove)
