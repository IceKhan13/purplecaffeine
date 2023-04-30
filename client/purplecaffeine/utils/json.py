"""Encoder / Decoder"""
import json
import pickle
from typing import Any
from qiskit.result import Result
from qiskit.providers import Backend
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit_ibm_runtime.utils import RuntimeEncoder, RuntimeDecoder

from purplecaffeine.trial import Trial


class TrialEncoder(json.JSONEncoder):
    """Json encoder."""

    def default(self, obj):
        """Default encoder class."""
        to_register = {}
        if isinstance(obj, Trial):
            trial_elem = [
                name_elem
                for name_elem in dir(obj)
                if not name_elem.startswith("__")
                and not name_elem.startswith("add_")
                and not name_elem.startswith("save_")
                and not name_elem.startswith("read_")
                and not name_elem == "backend"
            ]
            to_register = {
                f"{name_elem}": f"{self.tuple_encoder(getattr(obj, name_elem))}"
                for name_elem in trial_elem
            }
        return to_register

    @staticmethod
    def tuple_encoder(trial_elem: Any) -> Any:
        """Rules for tuple encoder."""
        to_append = []
        if len(trial_elem) == 0:
            return []
        if type(trial_elem[0]) is tuple:
            for obj_tuple in trial_elem:
                if (
                        isinstance(obj_tuple[1], str)
                        or isinstance(obj_tuple[1], int)
                        or isinstance(obj_tuple[1], float)
                ):
                    to_append.append((obj_tuple[0], obj_tuple[1]))
                elif isinstance(obj_tuple[1], QuantumCircuit):
                    to_append.append(
                        (obj_tuple[0], json.dumps(obj_tuple[1], cls=RuntimeEncoder))
                    )
                elif isinstance(obj_tuple[1], Backend):
                    to_append.append((obj_tuple[0], pickle.dumps(obj_tuple[1])))
                elif isinstance(obj_tuple[1], Operator):
                    to_append.append(
                        (obj_tuple[0], json.dumps(obj_tuple[1], cls=RuntimeEncoder))
                    )
                elif isinstance(obj_tuple[1], Result):
                    to_append.append(
                        (obj_tuple[0], json.dumps(obj_tuple[1], cls=RuntimeEncoder))
                    )
                else:
                    to_append.append((obj_tuple[0], pickle.dumps(obj_tuple[1])))
        else:
            to_append = trial_elem

        return to_append


class TrialDecoder(json.JSONDecoder):
    """Json decoder."""
