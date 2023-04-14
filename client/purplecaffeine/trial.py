"""Trial."""
import os
from typing import Optional, Union, List, Any
import numpy as np
from qiskit.providers import Backend
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from purplecaffeine.helpers import Configuration
from purplecaffeine.backend import BaseBackend, LocalBackend


class Trial:
    """Trial class."""

    def __init__(self, name: str, backend: Optional[BaseBackend] = None):
        """Trial class for tracking experiments data.

        Args:
            name: name of trial
            backend: backend to store data of trial. Default: local storage.
            metrics: list of metric, like number of qubits
            parameters: list of parameter, like env details
            circuits: list of quantum circuit
            qbackends: list of quantum backend
            operators: list of operator, like Pauli operators
            artifacts: list of artifact path, any external files path
            texts: list of text, any descriptions
            arrays: list of array, like quantum circuit results
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

    def add_array(self, array: Union[np.ndarray, List[Any]]):
        """Adds array to trial data.

        Args:
            array: quantum circuit results
        """
        self.arrays.append(array)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.backend.save_trial(self)
