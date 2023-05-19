"""Core."""
from __future__ import annotations

import glob
import json
import logging
import os
from pathlib import Path
from typing import Optional, Union, List, Any
from uuid import uuid4

import numpy as np
import requests
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
        uuid: Optional[str] = None,
        backend: Optional[BaseBackend] = None,
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
        self.uuid = uuid or str(uuid4())
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
        return f"<Trial [{self.name}] {self.uuid}>"

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
        self.backend.save(trial=self)

    def read(self, trial_id: str) -> Trial:
        """Read a trial from Backend.

        Args:
            trial_id: if backend is the remote api, you need the trial id find in database.

        Returns:
            Trial dict object
        """

        return self.backend.get(trial_id=trial_id)

    @staticmethod
    def import_from_shared_file(path) -> "Trial":
        """Import Trial for shared file.

        Args:
            path: full path of the file

        Returns:
            Trial dict object
        """
        with open(os.path.join(path), "r", encoding="utf-8") as trial_file:
            trial_json = json.load(trial_file, cls=TrialDecoder)
            if "id" in trial_json:
                del trial_json["id"]
            if "uuid" in trial_json:
                del trial_json["uuid"]
            return Trial(**trial_json)

    def export_to_shared_file(self, path) -> str:
        """Export trial to shared file.

        Args:
            path: path directory for the file

        Returns:
            Full path of the file
        """
        filename = os.path.join(path, f"{self.uuid}.json")
        with open(filename, "w", encoding="utf-8") as trial_file:
            json.dump(self.__dict__, trial_file, cls=TrialEncoder, indent=4)

        return filename

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()


class BaseBackend:
    """Base backend class."""

    def save(self, trial: Trial):
        """Saves given trial.

        Args:
            trial: encode trial to save
        """
        raise NotImplementedError

    def list(
        self,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> List[Trial]:
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

    def get(self, trial_id: str) -> Trial:
        """Returns trail by id.

        Args:
            trial_id: trial id

        Returns:
            trial: object of a trial
        """
        raise NotImplementedError


class ApiBackend(BaseBackend):
    """API backend class."""

    def __init__(self, username: str, password: str, host: str):
        """Creates backend for APIServer.

        Example:
            >>> backend = ApiBackend(
            >>>     host="http://localhost:8000/",
            >>>     username="admin",
            >>>     password="123"
            >>> )

        Args:
            username: username
            password: password
            host: host of api server
        """
        self.username = username
        self.host = host

        self.token = self._get_token(username, password)

    def _get_token(self, username: str, password: str) -> str:
        """Returns token based on username and password

        Returns:
            authorization token
        """
        raise NotImplementedError

    def save(self, trial: Trial):
        """Saves given trial.

        Args:
            trial: encode trial to save
        """
        requests.post(
            f"{Configuration.API_FULL_URL}/",
            headers=Configuration.API_HEADERS,
            json=json.loads(json.dumps(trial.__dict__, cls=TrialEncoder)),
            timeout=Configuration.API_TIMEOUT,
        )

        return trial.name

    def get(self, trial_id: str) -> Trial:
        """Returns trial by name.

        Args:
            trial_id: trial id

        Returns:
            trial: object of a trial
        """
        curl_req = requests.get(
            f"{Configuration.API_FULL_URL}/{trial_id}/",
            headers=Configuration.API_HEADERS,
            timeout=Configuration.API_TIMEOUT,
        )
        if "Not found." in str(curl_req.json()):
            raise ValueError(curl_req.json())

        trial_json = json.loads(json.dumps(curl_req.json()), cls=TrialDecoder)
        if "id" in trial_json:
            del trial_json["id"]
        if "uuid" in trial_json:
            del trial_json["uuid"]

        return Trial(**trial_json)

    def list(
        self,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> List[Trial]:
        """Returns list of trials.

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
        trials = []

        curl_req = requests.get(
            f"{Configuration.API_FULL_URL}/?query={query}&offset={offset}&limit={limit}/",
            headers=Configuration.API_HEADERS,
            timeout=Configuration.API_TIMEOUT,
        )
        for elem in curl_req.json():
            trial_json = json.loads(json.dumps(elem), cls=TrialDecoder)
            if "id" in trial_json:
                del trial_json["id"]
            if "uuid" in trial_json:
                del trial_json["uuid"]
            trials.append(trial_json)

        return trials


class LocalBackend(BaseBackend):
    """Local backend."""

    def __init__(self, path: str):
        """Creates local backend for storing trial data
        at local folder.

        Example:
            >>> backend = LocalBackend("./")

        Args:
            path: path for the local storage folder
        """
        self.path = path
        if not os.path.exists(self.path):
            Path(self.path).mkdir(parents=True, exist_ok=True)

    def save(self, trial: Trial) -> str:
        """Saves given trial.

        Args:
            trial: encode trial to save

        Returns:
            self.path: path of the trial file
        """
        save_path = os.path.join(self.path, f"{trial.uuid}.json")
        with open(save_path, "w", encoding="utf-8") as trial_file:
            json.dump(trial.__dict__, trial_file, cls=TrialEncoder, indent=4)

        return self.path

    def get(self, trial_id: str) -> Trial:
        """Read a given trial file.

        Args:
            trial_id: trial id

        Returns:
            trial: object of a trial
        """
        trial_path = os.path.join(self.path, f"{trial_id}.json")
        if not os.path.isfile(trial_path):
            logging.warning(
                "Your file %s does not exist.",
                trial_path,
            )
            raise ValueError(trial_id)
        with open(trial_path, "r", encoding="utf-8") as trial_file:
            return Trial(**json.load(trial_file, cls=TrialDecoder))

    def list(
        self,
        query: Optional[str] = None,  # pylint: disable=unused-argument
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> List[Trial]:
        """Returns list of trials.

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
                trial_dict = json.load(trial_file, cls=TrialDecoder)
                trials.append(Trial(**trial_dict))
        return trials
