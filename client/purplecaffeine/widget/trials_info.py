from purplecaffeine.core import LocalStorage, Trial, BaseStorage
from IPython.display import display, clear_output
from ipywidgets import Layout, GridspecLayout, AppLayout
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd

class Trials_info:
    def __init__(self, trial: Trial):
        self.trial = trial

    def set_trial(self, trial: Trial):
        self.trial = trial

    def display_empty(self):
        empty_message = widgets.HTML(
            f"<h1> Add a new trial to see the info of that trial </h1>")
        empty_message.layout = Layout(height = '300px')
        return empty_message

    def display_circuits(self):
        if(self.trial is None):
            return self.display_empty
        circuits = widgets.Output()
        with circuits:
            for name, circuit in self.selected_trial.circuits:
                print(name)
                print(circuit.draw())
        circuits.layout = Layout(overflow = 'scroll', max_height = '300px')

    def display_basic_info(self):
        if(self.trial is None):
            return self.display_empty
        parameter_rows = ''.join([
            f"<tr><td>{str(name)}</td><td><button class='btn btn-primary rounded-pill' disabled>{str(value)}</button></td></tr>"
            for name, value in self.selected_trial.parameters
        ])

        tags = ''.join([
            f"<button class='btn btn-primary rounded-pill btn-sm' style='margin-bottom:20px; margin-right: 10px' disabled>{str(tag)}</button>"
            for tag in self.selected_trial.tags
        ])
        info = widgets.HTML(
            f"<h3>{self.trial.name} | {self.trial.uuid} </h3>"
            f"<p>Description: {self.trial.description }</p>" 
            f"<div>{tags}</div>"
            "<table border=2 class='table'><tr><th>Parameter</th><th>Value</th></tr>"
            f"{parameter_rows}</table>")
        info.layout = Layout(overflow = 'scroll', max_height = '300px')
        return info
    
    def display_metrics(self):
        if(self.trial is None):
            return self.display_empty
        metrics = widgets.Output()
        with metrics:
            df = pd.DataFrame(self.selected_trial.metrics, columns=["name", "value"])
            df2 = df.groupby("name").agg(list)
            for metric_name, values in df2.to_dict()["value"].items():
                if len(values) == 1:
                    pass
                else:
                    plt.plot(values)
                    plt.xlabel("entry")
                    plt.ylabel("value")
                    plt.title(f"Metric: {metric_name}")
                    plt.show()
        metrics.layout = Layout(overflow = 'scroll', max_height = '300px')
        return metrics