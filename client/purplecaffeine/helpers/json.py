"""Encoder / Decoder"""
import ast
import json
from qiskit_ibm_runtime.utils import RuntimeEncoder, RuntimeDecoder


class Encoder:
    """Encoder class."""

    def __init__(self, trial):
        """Encoder class for serialization into json Trial."""
        self.json = {}
        circuits_encoder = []
        qbackends_encoder = []
        operators_encoder = []
        artifacts_encoder = []
        arrays_encoder = []

        for elem in trial.circuits:
            circuits_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        for elem in trial.operators:
            operators_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        for elem in trial.arrays:
            arrays_encoder.append((elem[0], json.dumps(elem[1], cls=RuntimeEncoder)))

        to_register = {
            "name": f"{trial.name}",
            "metrics": f"{trial.metrics}",
            "parameters": f"{trial.parameters}",
            "circuits": f"{circuits_encoder}",
            "qbackends": f"{qbackends_encoder}",
            "operators": f"{operators_encoder}",
            "artifacts": f"{artifacts_encoder}",
            "texts": f"{trial.texts}",
            "arrays": f"{arrays_encoder}",
            "tags": f"{trial.tags}",
        }

        self.json = json.dumps(to_register)


class Decoder:
    """Decoder class."""

    def __init__(self, payload: json):
        """Decoder class for deserialization of json Trial."""
        self.name = payload["name"]
        self.metrics = ast.literal_eval(payload["metrics"])
        self.parameters = ast.literal_eval(payload["parameters"])
        self.circuits = []
        self.qbackends = []
        self.operators = []
        self.artifacts = []
        self.texts = ast.literal_eval(payload["texts"])
        self.arrays = []
        self.tags = ast.literal_eval(payload["tags"])

        for elem in ast.literal_eval(payload["circuits"]):
            self.circuits.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
        for elem in ast.literal_eval(payload["operators"]):
            self.operators.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
        for elem in ast.literal_eval(payload["arrays"]):
            self.arrays.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
