"""Trial."""
import ast
import json
import pickle
import logging
from typing import Optional, Union, List, Any
import numpy as np
from pympler import asizeof
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
            artifacts: list of artifact, any external files
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

    def add_artifact(self, name: str, artifact: Any):
        """Adds artifacts path to trial data.

        Args:
            name: name of the file
            artifact: file object
        """
        if asizeof.asizeof(artifact) >= Configuration.MAX_SIZE:
            logging.warning(
                "Your file is too big ! Limit : "
                + str(Configuration.MAX_SIZE)
                + " Bytes"
            )
        self.artifacts.append((name, artifact))

    def add_text(self, title: str, text: str):
        """Adds any text to trial data.

        Args:
            title: title of the text
            text: long string
        """
        self.texts.append((title, text))

    def add_array(self, name: str, array: Union[np.ndarray, List[Any]]):
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
        """Serialize Trial into Json format and save into Backend."""
        circuits_encoder = []
        for elem in self.circuits:
            circuits_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        qbackends_encoder = []
        for elem in self.qbackends:
            qbackends_encoder.append((elem[0], pickle.dumps(elem[1])))

        operators_encoder = []
        for elem in self.operators:
            operators_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        artifacts_encoder = []
        for elem in self.artifacts:
            artifacts_encoder.append((elem[0], pickle.dumps(elem[1])))

        arrays_encoder = []
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

        trial = json.dumps(to_register)
        self.backend.save_trial(name=self.name, trial=trial)

    def read_trial(self):
        """Read a trial from Backend & deserialize it into Trial object."""
        trial = self.backend.read_trial(name=self.name)

        self.name = trial["name"]
        self.metrics = ast.literal_eval(trial["metrics"])
        self.parameters = ast.literal_eval(trial["parameters"])

        self.circuits = []
        for elem in ast.literal_eval(trial["circuits"]):
            self.circuits.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))

        self.qbackends = []
        for elem in ast.literal_eval(trial["qbackends"]):
            self.qbackends.append((elem[0], pickle.loads(elem[1])))

        self.operators = []
        for elem in ast.literal_eval(trial["operators"]):
            self.operators.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))

        self.artifacts = []
        for elem in ast.literal_eval(trial["artifacts"]):
            self.artifacts.append((elem[0], pickle.loads(elem[1])))

        self.texts = ast.literal_eval(trial["texts"])

        self.arrays = []
        for elem in ast.literal_eval(trial["arrays"]):
            self.arrays.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))

        self.tags = ast.literal_eval(trial["tags"])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_trial()
