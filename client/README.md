PurpleCaffeine: tracking of quantum programs and experiments
============================================================

![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-informational)
[![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-informational)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-%E2%89%A5%200.34.2-6133BD)](https://github.com/Qiskit/qiskit)
[![License](https://img.shields.io/github/license/qiskit-community/quantum-prototype-template?label=License)](https://github.com/IceKhan13/purplecaffeine/blob/main/LICENSE)
[![Code style: Black](https://img.shields.io/badge/Code%20style-Black-000.svg)](https://github.com/psf/black)

![Logo](https://raw.githubusercontent.com/IceKhan13/purplecaffeine/main/docs/images/readme_logo.png)

Tracking experiments and programs is known problem in scientific community.
This project is aimed to create simple general interface to track quantum experiments, store and search them in an easy way.

### Table of Contents

##### For Users

1. [Quickstart](#quickstart)
2. [Documentation](#documentation)
3. [Guides](https://github.com/IceKhan13/purplecaffeine/tree/main/docs/guides)
4. [How to Give Feedback](#how-to-give-feedback)
5. [Contribution Guidelines](#contribution-guidelines)
6. [References and Acknowledgements](#references-and-acknowledgements)
7. [License](#license)


----------------------------------------------------------------------------------------------------

### Quickstart

```python
from qiskit.circuit.random import random_circuit
from qiskit.quantum_info.random import random_pauli
from qiskit.primitives import Estimator

from purplecaffeine.core import Trial, LocalStorage
from purplecaffeine.widget import Widget

n_qubits = 4
depth = 3
shots = 2000

circuit = random_circuit(n_qubits, depth)
obs = random_pauli(n_qubits)

local_storage = LocalStorage("./")

with Trial("Example trial", storage=local_storage) as trial:
    # track some parameters
    trial.add_parameter("estimator", "qiskit.primitives.Estimator")
    trial.add_parameter("depth", depth)
    trial.add_parameter("n_qubits", n_qubits)
    trial.add_parameter("shots", shots)
    
    # track objects of interest
    trial.add_circuit("circuit", circuit)
    trial.add_operator("obs", obs)

    # run
    exp_value = Estimator().run(circuit, obs, shots=shots).result().values.item()
    
    # track results of run
    trial.add_metric("exp_value", exp_value)

Widget(local_storage).show()
```
![visualization](https://raw.githubusercontent.com/IceKhan13/purplecaffeine/main/docs/images/visualization.png)

----------------------------------------------------------------------------------------------------

### Documentation

Documentation for project is hosted at https://icekhan13.github.io/purplecaffeine/

----------------------------------------------------------------------------------------------------

### How to Give Feedback

We encourage your feedback! You can share your thoughts with us by:
- [Opening an issue](https://github.com/IceKhan13/purplecaffeine/issues) in the repository


----------------------------------------------------------------------------------------------------

### Contribution Guidelines

For information on how to contribute to this project, please take a look at our [contribution guidelines](https://github.com/IceKhan13/purplecaffeine/blob/main/CONTRIBUTING.md).


----------------------------------------------------------------------------------------------------

## References and Acknowledgements
[1] Qiskit is an open-source SDK for working with quantum computers at the level of circuits, algorithms, and application modules. \
    https://github.com/Qiskit/qiskit


----------------------------------------------------------------------------------------------------

### License
[Apache License 2.0](LICENSE)
