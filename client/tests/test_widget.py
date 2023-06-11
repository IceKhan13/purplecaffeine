"""Tests for Trial."""
import os
import shutil
from pathlib import Path
from typing import Optional
from unittest import TestCase

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate
from qiskit.quantum_info import Operator

from purplecaffeine import Trial, LocalStorage, BaseStorage as TrialStorage

from typing import List, Optional

import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, clear_output
from ipywidgets import Layout, GridspecLayout, AppLayout

from purplecaffeine.core import BaseStorage, LocalStorage, Trial

from purplecaffeine.widget import Widget


class TestWidget(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp Trial object."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(current_directory, "resources")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_storage = LocalStorage(path=self.save_path)
        

    def test_empty_string(self):
        widget = Widget(self.local_storage)
        """Test when we don't have trials."""
        empty_string_displayed = (f"<h1 style='text-align: center;'> <br><br><br>Add a new trial to see the info of that trial </h1>"
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">')
        self.assertEqual(widget.display_empty().value, empty_string_displayed)
