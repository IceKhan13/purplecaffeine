"""Encoder / Decoder"""
import pickle
from typing import Any

from qiskit.providers import Backend
from qiskit_ibm_runtime.utils import RuntimeEncoder, RuntimeDecoder


# pylint: disable=no-else-return, import-outside-toplevel, cyclic-import
class TrialEncoder(RuntimeEncoder):
    """Json encoder for trial."""

    def default(self, obj: Any) -> Any:
        "custom encoder"
        from purplecaffeine.core import BaseStorage

        if isinstance(obj, Backend):
            return {
                "__type__": "Backend",
                "__value__": pickle.dumps(obj),
            }
        elif isinstance(obj, BaseStorage):
            return {"__type__": "PurpleCaffeineStorage"}
        return super().default(obj)


class TrialDecoder(RuntimeDecoder):
    """Json decoder for trial."""

    def object_hook(self, obj: Any) -> Any:
        "custom decoder"
        if "__type__" in obj:
            obj_type = obj["__type__"]

            if obj_type == "Backend":
                return pickle.loads(obj["__value__"])
            elif obj_type == "PurpleCaffeineStorage":
                # we should not recover trial backend
                return None
            return super().object_hook(obj)
        return obj
