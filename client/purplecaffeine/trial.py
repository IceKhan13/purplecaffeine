"""Trial."""
import logging
from typing import Optional, Union, List, Any
import numpy as np
from pympler import asizeof
from qiskit.providers import Backend
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from purplecaffeine.helpers import Configuration
from purplecaffeine.backend import BaseBackend, LocalBackend


class Trial:
    """Trial class.

    Attributes:
        metrics (List[(str, Union[int, float])]): list of metric, like number of qubits
        parameters (List[(str, str)]): list of parameter, like env details
        circuits (List[(str, QuantumCircuit)]): list of quantum circuit
        qbackends (List[(str, Backend)]): list of quantum backend
        operators (List[(str, Operator)]): list of operator, like Pauli operators
        artifacts (List[(str, Any)]): list of artifact, any external files
        texts (List[(str, str)]): list of text, any descriptions
        arrays (List[(str, Union[np.ndarray, List[Any]])]):
            list of array, like quantum circuit results
        tags (List[str]): list of tags in string format
    """

    def __init__(self, name: str, backend: Optional[BaseBackend] = None):
        """Trial class for tracking experiments data.

        Args:
            name: name of trial
            backend: backend to store data of trial. Default: local storage.
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
                "Your file is too big ! Limit : %s Bytes", str(Configuration.MAX_SIZE)
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
        """Save into Backend."""
        self.backend.save_trial(name=self.name, trial=self)

    def read_trial(self) -> dict:
        """Read a trial from Backend.

        Returns:
            Trial dict object
        """
        return self.backend.read_trial(name=self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_trial()
