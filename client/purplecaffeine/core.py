"""Core."""
import glob
import json
import logging
import os
from typing import Optional, Union, List, Any

import numpy as np
from pympler import asizeof
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from purplecaffeine.helpers import Configuration
from purplecaffeine.utils import TrialEncoder, TrialDecoder


class Trial:
    """Trial class.

    Attributes:
        metrics (List[(str, Union[int, float])]): list of metric, like number of qubits
        parameters (List[(str, str)]): list of parameter, like env details
        circuits (List[(str, QuantumCircuit)]): list of quantum circuit
        operators (List[(str, Operator)]): list of operator, like Pauli operators
        artifacts (List[(str, Any)]): list of artifact, any external files
        texts (List[(str, str)]): list of text, any descriptions
        arrays (List[(str, Union[np.ndarray, List[Any]])]):
            list of array, like quantum circuit results
        tags (List[str]): list of tags in string format
    """

    def __init__(
        self,
        name: str,
        backend: Optional["BaseBackend"] = None,
        metrics: Optional[List[List[Union[str, float]]]] = None,
        parameters: Optional[List[List[str]]] = None,
        circuits: Optional[List[List[Union[str, QuantumCircuit]]]] = None,
        operators: Optional[List[List[Union[str, Operator]]]] = None,
        artifacts: Optional[List[List[str]]] = None,
        texts: Optional[List[List[str]]] = None,
        arrays: Optional[List[List[Union[str, np.ndarray]]]] = None,
        tags: Optional[List[str]] = None,
    ):
        """Trial class for tracking experiments data.

        Args:
            name: name of trial
            backend: backend to store data of trial. Default: local storage.
        """
        self.name = name
        self.backend = backend or LocalBackend(path="./")

        self.metrics = metrics or []
        self.parameters = parameters or []
        self.circuits = circuits or []
        self.operators = operators or []
        self.artifacts = artifacts or []
        self.texts = texts or []
        self.arrays = arrays or []
        self.tags = tags or []

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
        self.metrics.append([name, value])

    def add_parameter(self, name: str, value: str):
        """Adds parameter to trial data.

        Args:
            name: name of the parameter, like OS
            value: value for the parameter, like Ubuntu
        """
        self.parameters.append([name, value])

    def add_circuit(self, name: str, circuit: QuantumCircuit):
        """Adds circuit to trial data.

        Args:
            name: name of the circuit
            circuit: QuantumCircuit
        """
        self.circuits.append([name, circuit])

    def add_operator(self, name: str, operator: Operator):
        """Adds operator to trial data.

        Args:
            name: name of the parameter
            operator: quantum Operator
        """
        self.operators.append([name, operator])

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
        self.artifacts.append([name, artifact])

    def add_text(self, title: str, text: str):
        """Adds any text to trial data.

        Args:
            title: title of the text
            text: long string
        """
        self.texts.append([title, text])

    def add_array(self, name: str, array: Union[np.ndarray, List[Any]]):
        """Adds array to trial data.

        Args:
            name: name of the array
            array: quantum circuit results
        """
        self.arrays.append([name, array])

    def add_tag(self, tag: str):
        """Adds any tag to trial data.

        Args:
            tag: word of your tag
        """
        self.tags.append(tag)

    def save(self):
        """Save into Backend."""
        self.backend.save(name=self.name, trial=self)

    def read_trial(self) -> "Trial":
        """Read a trial from Backend.

        Returns:
            Trial dict object
        """
        return self.backend.get(name=self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()


class BaseBackend:
    """Base backend class."""

    def save(self, name: str, trial: Trial):
        """Saves given trial.

        Args:
            name: name of the trial
            trial: encode trial to save
        """
        raise NotImplementedError

    def list(
        self,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> List["Trial"]:
        """Returns list of trails.

        Args:
            query: search query
            limit: limit
            offset: offset
            **kwargs: other filtering criteria

        Returns:
            list of trials
        """
        raise NotImplementedError

    def get(self, name: str) -> "Trial":
        """Returns trail by name.

        Args:
            name: trail name

        Returns:
            trial by given name
        """
        raise NotImplementedError


class LocalBackend(BaseBackend):
    """Local backend."""

    def __init__(self, path: str):
        self.path = path

    def save(self, name: str, trial) -> str:
        """Saves given trial.

        Args:
            name: name of the trial
            trial: encode trial to save

        Returns:
            self.path: path of the trial file
        """
        with open(
            os.path.join(self.path, name + ".json"), "w", encoding="utf-8"
        ) as trial_file:
            json.dump(trial.__dict__, trial_file, cls=TrialEncoder, indent=4)

        return self.path

    def get(self, name: str) -> "Trial":
        """Read a given trial file.

        Args:
            name: name of the trial

        Returns:
            trial: object of a trial
        """
        with open(
            os.path.join(self.path, name + ".json"), "r", encoding="utf-8"
        ) as trial_file:
            return Trial(**json.load(trial_file, cls=TrialDecoder))

    def list(
        self,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> List["Trial"]:
        """Returns list of trails.

        Args:
            query: search query
            limit: limit
            offset: offset
            **kwargs: other filtering criteria

        Returns:
            list of trials
        """
        offset = offset or 0
        limit = limit or 10

        trails_path = glob.glob(f"{self.path}/**.json")[offset:limit]
        trials = []
        for path in trails_path:
            with open(path, "r", encoding="utf-8") as trial_file:
                trials.append(json.load(trial_file, cls=TrialDecoder))
        return trials