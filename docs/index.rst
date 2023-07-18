##############
PurpleCaffeine
##############

PurpleCaffeine is a software for tracking quantum programs and experiments.

.. image:: /images/readme_logo.png

The source code to the project is available `on GitHub <https://github.com/IceKhan13/purplecaffeine>`_.

------------

**Quickstart**

Step 0: install package

.. code-block::
   :caption: pip install

      pip install purplecaffeine


Step 1: run experiment

.. code-block:: python
   :caption: script.py

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

      # store experiment data locally in `trials` folder
      local_storage = LocalStorage("./trials")

      # open trial context to track experiment data
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


Step 2: visualize tracked data

.. code-block:: python
   :caption: script.py

      Widget(local_storage).show()

.. image:: /images/visualization.png

------------

**Content**

.. toctree::
  :maxdepth: 2

  Documentation Home <self>

.. toctree::
  :maxdepth: 2
  :caption: Guides

  Guides <guides/index>

.. toctree::
  :maxdepth: 2
  :caption: API references

  API References <apidocs/index>

.. Hiding - Indices and tables
   :ref:`genindex`
   :ref:`modindex`
   :ref:`search`
