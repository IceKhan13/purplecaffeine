"""Trial."""
import os
import ast
import json
from typing import Optional, Union, List, Any
import numpy as np
from qiskit.providers import Backend
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit_ibm_runtime.utils import RuntimeEncoder, RuntimeDecoder

from purplecaffeine.helpers import Configuration
from purplecaffeine.backend import BaseBackend, LocalBackend


class Trial:
    """Trial class."""

    def __init__(self, name: str, backend: Optional[BaseBackend] = None):
        """Trial class for tracking experiments data.

        Args:
            name: name of trial
            backend: backend to store data of trial. Default: local storage.

        Properties:
            metrics: list of metric, like number of qubits
            parameters: list of parameter, like env details
            circuits: list of quantum circuit
            qbackends: list of quantum backend
            operators: list of operator, like Pauli operators
            artifacts: list of artifact path, any external files path
            texts: list of text, any descriptions
            arrays: list of array, like quantum circuit results
            tags: list of tags in string format
        """
        self.name = name
        self.backend = backend or LocalBackend(path="./")

        self.metrics = []
        self.parameters = []
        self.circuits = []
        self.qbackends = []
        self.operators = []
        self.artifacts = []
        self.texts = []
        self.arrays = []
        self.tags = []

    def __repr__(self):
        return f"<Trial: {self.name}>"

    def __enter__(self):
        return self

    def add_metric(self, name: str, value: Union[int, float]):
        """Adds metric to trial data.

        Args:
            name: name of metric
            value: value of metric
        """
        self.metrics.append((name, value))

    def add_parameter(self, name: str, value: str):
        """Adds parameter to trial data.

        Args:
            name: name of the parameter, like OS
            value: value for the parameter, like Ubuntu
        """
        self.parameters.append((name, value))

    def add_circuit(self, name: str, circuit: QuantumCircuit):
        """Adds circuit to trial data.

        Args:
            name: name of the circuit
            circuit: QuantumCircuit
        """
        self.circuits.append((name, circuit))

    def add_qbackend(self, name: str, backend: Backend):
        """Adds quantum backend to trial data.

        Args:
            name: name of the backend
            backend: quantum Backend
        """
        self.qbackends.append((name, backend))

    def add_operator(self, name: str, operator: Operator):
        """Adds operator to trial data.

        Args:
            name: name of the parameter
            operator: quantum Operator
        """
        self.operators.append((name, operator))

    def add_artifact(self, name: str, path_to_file: str):
        """Adds artifacts path to trial data.

        Args:
            name: name of the file
            path_to_file: path to access to the file
        """
        if os.stat(path_to_file).st_size >= Configuration.MAX_SIZE:
            print(
                "Your file is too big ! Limit : "
                + str(Configuration.MAX_SIZE)
                + " Bytes"
            )
        self.artifacts.append((name, path_to_file))

    def add_text(self, title: str, text: str):
        """Adds any text to trial data.

        Args:
            title: title of the text
            text: long string
        """
        self.texts.append((title, text))

    def add_array(self, name, array: Union[np.ndarray, List[Any]]):
        """Adds array to trial data.

        Args:
            name: name of the array
            array: quantum circuit results
        """
        self.arrays.append((name, array))

    def add_tag(self, tag: str):
        """Adds any tag to trial data.

        Args:
            tag: word of your tag
        """
        self.tags.append(tag)

    def save_trial(self):
        """Save a trial into Backend."""
        circuits_encoder = []
        qbackends_encoder = []
        operators_encoder = []
        artifacts_encoder = []
        arrays_encoder = []

        for elem in self.circuits:
            circuits_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        for elem in self.operators:
            operators_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        for elem in self.arrays:
            arrays_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        to_register = {
            "name": f"{self.name}",
            "metrics": f"{self.metrics}",
            "parameters": f"{self.parameters}",
            "circuits": f"{circuits_encoder}",
            "qbackends": f"{qbackends_encoder}",
            "operators": f"{operators_encoder}",
            "artifacts": f"{artifacts_encoder}",
            "texts": f"{self.texts}",
            "arrays": f"{arrays_encoder}",
            "tags": f"{self.tags}",
        }

        trial_json = json.dumps(to_register)
        self.backend.save_trial(name=self.name, trial_json=trial_json)

    def read_trial(self):
        """Read a trial from Backend."""
        self.circuits = []
        self.qbackends = []
        self.operators = []
        self.artifacts = []
        self.arrays = []
        trial_json = self.backend.read_trial(name=self.name)

        self.name = trial_json["name"]
        self.metrics = ast.literal_eval(trial_json["metrics"])
        self.parameters = ast.literal_eval(trial_json["parameters"])
        for elem in ast.literal_eval(trial_json["circuits"]):
            self.circuits.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
        self.qbackends = []
        for elem in ast.literal_eval(trial_json["operators"]):
            self.operators.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
        self.artifacts = []
        self.texts = ast.literal_eval(trial_json["texts"])
        for elem in ast.literal_eval(trial_json["arrays"]):
            self.arrays.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
        self.tags = ast.literal_eval(trial_json["tags"])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_trial()
