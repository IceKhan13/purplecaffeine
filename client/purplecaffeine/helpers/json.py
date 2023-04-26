"""Encoder / Decoder"""
import ast
import json
from qiskit_ibm_runtime.utils import RuntimeEncoder, RuntimeDecoder


class Encoder:
    """"""

    def __init__(self, trial):
        """"""
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
        }

        self.json = json.dumps(to_register)


class Decoder:
    """"""

    def __init__(self, payload: json):
        """"""
        self.name = payload["name"]
        self.metrics = ast.literal_eval(payload["metrics"])
        self.parameters = ast.literal_eval(payload["parameters"])
        self.circuits = []
        self.qbackends = []
        self.operators = []
        self.artifacts = []
        self.texts = ast.literal_eval(payload["texts"])
        self.arrays = []

        for elem in ast.literal_eval(payload["circuits"]):
            self.circuits.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
        for elem in ast.literal_eval(payload["operators"]):
            self.operators.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
        for elem in ast.literal_eval(payload["arrays"]):
            self.arrays.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))


