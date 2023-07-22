"""Core."""
from __future__ import annotations

import glob
import json
import logging
import os
from pathlib import Path
from typing import Optional, Union, List, Any, Dict
from uuid import uuid4

import boto3
import numpy as np
import requests
from pympler import asizeof
from qiskit import __qiskit_version__
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from purplecaffeine.exception import PurpleCaffeineException
from purplecaffeine.helpers import Configuration
from purplecaffeine.utils import TrialEncoder, TrialDecoder


class Trial:
    """Trial class.

    Attributes:
        description (str): short description of the trial
        metrics (List[(str, Union[int, float])]): list of metric, like number of qubits
        parameters (List[(str, str)]): list of parameter, like env details
        circuits (List[(str, QuantumCircuit)]): list of quantum circuit
        operators (List[(str, Operator)]): list of operator, like Pauli operators
        artifacts (List[(str, Any)]): list of artifact, any external files
        texts (List[(str, str)]): list of text, any descriptions
        arrays (List[(str, Union[np.ndarray, List[Any]])]):
            list of array, like quantum circuit results
        tags (List[str]): list of tags in string format
        versions (List[(str, str)]): list of qiskit version
    """

    def __init__(
        self,
        name: str,
        uuid: Optional[str] = None,
        storage: Optional[BaseStorage] = None,
        description: Optional[str] = None,
        metrics: Optional[List[List[Union[str, float]]]] = None,
        parameters: Optional[List[List[str]]] = None,
        circuits: Optional[List[List[Union[str, QuantumCircuit]]]] = None,
        operators: Optional[List[List[Union[str, Operator]]]] = None,
        artifacts: Optional[List[List[str]]] = None,
        texts: Optional[List[List[str]]] = None,
        arrays: Optional[List[List[Union[str, np.ndarray]]]] = None,
        tags: Optional[List[str]] = None,
        versions: Optional[List[List[str]]] = None,
    ):
        """Trial class for tracking experiments data.

        Args:
            description (str): short description of the trial
            metrics (List[(str, Union[int, float])]): list of metric, like number of qubits
            parameters (List[(str, str)]): list of parameter, like env details
            circuits (List[(str, QuantumCircuit)]): list of quantum circuit
            operators (List[(str, Operator)]): list of operator, like Pauli operators
            artifacts (List[(str, Any)]): list of artifact, any external files
            texts (List[(str, str)]): list of text, any descriptions
            arrays (List[(str, Union[np.ndarray, List[Any]])]):
                list of array, like quantum circuit results
            tags (List[str]): list of tags in string format
            versions (List[(str, str)]): list of qiskit version
        """
        self.uuid = uuid or str(uuid4())
        self.name = name or os.environ.get("PURPLE_CAFFEINE_TRIAL_NAME")
        if self.name is None:
            raise PurpleCaffeineException(
                "Please specify name of trial or configure it using env variables"
            )

        if storage is None:
            storage_type = os.environ.get(
                "PURPLE_CAFFEINE_STORAGE_CLASS", "LocalStorage"
            )
            storage_mapping: Dict[str, BaseStorage] = {
                "LocalStorage": LocalStorage,
                "S3Storage": S3Storage,
                "ApiStorage": ApiStorage,
            }
            self.storage = storage_mapping.get(storage_type)()
        else:
            self.storage = storage

        self.description = description or os.environ.get(
            "PURPLE_CAFFEINE_TRIAL_DESCRIPTION", ""
        )
        self.metrics = metrics or []
        self.parameters = parameters or []
        self.circuits = circuits or []
        self.operators = operators or []
        self.artifacts = artifacts or []
        self.texts = texts or []
        self.arrays = arrays or []
        self.tags = tags or (
            os.environ.get("PURPLE_CAFFEINE_TRIAL_TAGS", "").split(",")
            if os.environ.get("PURPLE_CAFFEINE_TRIAL_TAGS")
            else []
        )
        self.versions = versions or []

    def __repr__(self):
        return f"<Trial [{self.name}] {self.uuid}>"

    def __enter__(self):
        return self

    def add_description(self, description: str):
        """Add description to trial data.

        Args:
            description: short description of the trial
        """
        self.description = description

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

    def add_version(self, name: str, value: str):
        """Adds version to trial data.

        Args:
            name: name of the package
            value: version for the package
        """
        self.versions.append([name, value])

    def save(self):
        """Save into Storage."""
        self.storage.save(trial=self)

    def read(self, trial_id: str) -> Trial:
        """Read a trial from Storage.

        Args:
            trial_id: if storage is the remote api, you need the trial id find in database,
                else you have to use the uuid.

        Returns:
            Trial dict object
        """

        return self.storage.get(trial_id=trial_id)

    @staticmethod
    def import_from_shared_file(path) -> Trial:
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
        for key in __qiskit_version__:
            self.add_version(key, __qiskit_version__[key])
        self.save()


class BaseStorage:
    """Base storage class."""

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
        """Returns list of trials.

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


class ApiStorage(BaseStorage):
    """API storage class."""

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
    ):
        """Creates storage for APIServer.

        Example:
            >>> storage = ApiStorage(
            >>>     host="http://localhost:8000/",
            >>>     username="admin",
            >>>     password="123"
            >>> )

        Args:
            username: username
            password: password
            host: host of api server
        """
        self.username = username or os.environ.get(
            "PURPLE_CAFFEINE_API_STORAGE_USERNAME"
        )
        if self.username is None:
            raise PurpleCaffeineException(
                "Please specify api storage username or configure it using env variables"
            )
        self.password = password or os.environ.get(
            "PURPLE_CAFFEINE_API_STORAGE_PASSWORD"
        )
        if self.password is None:
            raise PurpleCaffeineException(
                "Please specify api storage Password or configure it using env variables"
            )
        self.host = host or os.environ.get("PURPLE_CAFFEINE_API_STORAGE_HOST")
        if self.host is None:
            raise PurpleCaffeineException(
                "Please specify api storage host or configure it using env variables"
            )

        self.token = self._get_token(self.username, self.password)

    def _get_token(self, username: str, password: str) -> str:
        """Returns token based on username and password

        Returns:
            authorization token
        """
        payload = {"username": f"{username}", "password": f"{password}"}
        curl_req = requests.post(
            f"{self.host}/{Configuration.API_TOKEN_ENDPOINT}/",
            headers=Configuration.API_HEADERS,
            json=payload,
            timeout=Configuration.API_TIMEOUT,
        )

        return curl_req.json()["access"]

    def save(self, trial: Trial):
        """Saves given trial.

        Args:
            trial: encode trial to save
        """
        requests.post(
            f"{self.host}/{Configuration.API_TRIAL_ENDPOINT}/",
            headers={
                **Configuration.API_HEADERS,
                "Authorization": f"Bearer {self.token}",
            },
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
            f"{self.host}/{Configuration.API_TRIAL_ENDPOINT}/{trial_id}/",
            headers={
                **Configuration.API_HEADERS,
                "Authorization": f"Bearer {self.token}",
            },
            timeout=Configuration.API_TIMEOUT,
        )
        if "Not found." in str(curl_req.json()):
            raise ValueError(curl_req.json())

        trial_json = json.loads(json.dumps(curl_req.json()), cls=TrialDecoder)
        if "id" in trial_json:
            del trial_json["id"]

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
            f"""
                {self.host}/{Configuration.API_TRIAL_ENDPOINT}/
                ?query={query}&offset={offset}&limit={limit}/
            """,
            headers={
                **Configuration.API_HEADERS,
                "Authorization": f"Bearer {self.token}",
            },
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


class LocalStorage(BaseStorage):
    """Local storage."""

    def __init__(self, path: Optional[str] = None):
        """Creates local storage for storing trial data
        at local folder.

        Example:
            >>> storage = LocalStorage("./")

        Args:
            path: path for the local storage folder
        """
        self.path = path or os.environ.get("PURPLE_CAFFEINE_LOCAL_STORAGE_PATH", "./")
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
            trial_id: trial uuid

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

        trials_path = glob.glob(f"{self.path}/**.json")
        trials_path.sort(key=os.path.getmtime, reverse=True)
        trials = []
        for path in trials_path:
            with open(path, "r", encoding="utf-8") as trial_file:
                trial_dict = json.load(trial_file, cls=TrialDecoder)
                trials.append(Trial(**trial_dict))

        if query:
            trials = [
                trial
                for trial in trials
                if (query in trial.tags)
                or (trial.name.find(query) != -1)
                or (trial.description.find(query) != -1)
            ]

        trials = trials[offset : offset + limit]
        return trials


class S3Storage(BaseStorage):
    """S3 storage."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        directory: Optional[str] = None,
        endpoint_url: Optional[str] = None,
    ):
        """Storage storage for s3 buckets.

        Allows to store trial data inside s3 buckets.

        Example:
            >>> storage = S3Storage("my_bucket", key="<AWS_KEY>", access_key="<AWS_ACCESS_KEY>")

        Args:
            bucket_name: bucket name
            access_key: aws key
            secret_access_key: aws access key
            directory: optional directory within bucket
            endpoint_url: optional endpoint url for custom S3 location
        """
        self.bucket_name = bucket_name or os.environ.get("PURPLE_CAFFEINE_S3_BUCKET")
        if self.bucket_name is None:
            raise PurpleCaffeineException(
                "Please specify name of S3 Bucket or configure it using env variables"
            )
        self.access_key = os.environ.get("PURPLE_CAFFEINE_S3_ACCESS_KEY")
        if access_key is not None:
            self.access_key = access_key

        self.secret_access_key = os.environ.get("PURPLE_CAFFEINE_S3_SECRET_ACCESS_KEY")
        if secret_access_key is not None:
            self.secret_access_key = secret_access_key

        if self.secret_access_key is None or self.access_key is None:
            raise PurpleCaffeineException(
                "Please specify Access key of S3 Bucket or configure it using env variables"
            )
        self.directory = directory or os.environ.get("PURPLE_CAFFEINE_S3_DIRECTORY")
        self.endpoint_url = endpoint_url or os.environ.get(
            "PURPLE_CAFFEINE_S3_ENDPOINT"
        )
        client_s3 = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key,
            endpoint_url=endpoint_url,
        )
        self.client_s3 = client_s3

    def save(self, trial: Trial) -> str:
        """Saves given trial.

        Args:
            trial: trial to save

        Returns:
            trial.uuid: key of the trial
        """
        trial_data = json.dumps(trial.__dict__, cls=TrialEncoder, indent=4)
        response: Dict[str, Any] = self.client_s3.put_object(
            Bucket=self.bucket_name, Key=trial.uuid, Body=trial_data
        )
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        if status != 200:
            raise PurpleCaffeineException(
                f"Error response from boto client on attempt to write trial: {response}"
            )
        return trial.uuid

    def get(self, trial_id: str) -> Trial:
        """Read a given trial file.

        Args:
            trial_id: trial id

        Returns:
            trial: object of a trial
        """
        try:
            response: Dict[str, Any] = self.client_s3.get_object(
                Bucket=self.bucket_name, Key=trial_id
            )
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
            if status != 200:
                raise PurpleCaffeineException(
                    f"Error response from boto client on attempt to read trial: {response}"
                )
            return Trial(**json.loads(response["Body"].read(), cls=TrialDecoder))
        except Exception as get_exception:
            raise PurpleCaffeineException from get_exception

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
        paginator = self.client_s3.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=self.bucket_name,
            PaginationConfig={"MaxItems": offset + limit, "PageSize": limit},
        )
        for page, result in enumerate(page_iterator):
            if "Contents" in result:
                for idx, s3_object in enumerate(result["Contents"]):
                    file_offset = page * limit + idx
                    if file_offset >= offset:
                        trial = self.get(s3_object["Key"])
                        trials.append(trial)

        return trials
