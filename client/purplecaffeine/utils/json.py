"""Encoder / Decoder"""
import ast
import json
import pickle
from typing import Any
from qiskit.result import Result
from qiskit.providers import Backend
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit_ibm_runtime.utils import RuntimeEncoder, RuntimeDecoder

from purplecaffeine.trial import Trial


def filtered_attr(obj: Trial) -> []:
    return [
        name_elem
        for name_elem in dir(obj)
        if not name_elem.startswith("__")
        and not name_elem.startswith("add_")
        and not name_elem.startswith("save_")
        and not name_elem.startswith("read_")
        and not name_elem == "backend"
        and not name_elem == "name"
    ]


class TrialEncoder(json.JSONEncoder):
    """Json encoder."""

    def default(self, obj):
        """Default encoder class."""
        to_register = {}
        if isinstance(obj, Trial):
            trial_elem = filtered_attr(obj=obj)
            to_register = {
                f"name": f"{obj.name}",
                **{
                    f"{name_elem}": f"{self.tuple_encoder(getattr(obj, name_elem))}"
                    for name_elem in trial_elem
                },
            }
        return to_register

    @staticmethod
    def tuple_encoder(trial_elem: Any) -> Any:
        """Rules for encoder."""
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

    def __init__(self, *args, **kwargs):
        """Decoder call."""
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(obj: json):
        """Rules for decoder."""
        new_trial = Trial(obj["name"])
        trial_elem = filtered_attr(obj=new_trial)
        for attr in trial_elem:
            to_value = []
            if len(ast.literal_eval(obj[attr])) == 0:
                setattr(new_trial, attr, to_value)

            elif attr == "circuits":
                for elem in ast.literal_eval(obj[attr]):
                    to_value.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
                setattr(new_trial, attr, to_value)
            elif attr == "qbackends":
                for elem in ast.literal_eval(obj[attr]):
                    to_value.append((elem[0], pickle.loads(elem[1])))
                setattr(new_trial, attr, to_value)
            elif attr == "operators":
                for elem in ast.literal_eval(obj[attr]):
                    to_value.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
                setattr(new_trial, attr, to_value)
            elif attr == "artifacts":
                for elem in ast.literal_eval(obj[attr]):
                    to_value.append((elem[0], pickle.loads(elem[1])))
                setattr(new_trial, attr, to_value)
            elif attr == "arrays":
                for elem in ast.literal_eval(obj[attr]):
                    to_value.append((elem[0], json.loads(elem[1], cls=RuntimeDecoder)))
                setattr(new_trial, attr, to_value)

            else:
                setattr(new_trial, attr, ast.literal_eval(obj[attr]))

        return new_trial
