from typing import List, Optional

import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, clear_output
from ipywidgets import Layout, GridspecLayout

from purplecaffeine.core import LocalStorage, Trial, BaseStorage


class Widget:
    def __init__(self, storage: Optional[BaseStorage] = None):
        self.storage = storage or LocalStorage("./trials")
        self.limit = 10
        self.offset = 0
        self.trials: List[Trial] = self.storage.list(limit=self.limit, offset=self.offset)
        self.selected_trial: Optional[Trial] = self.trials[0] if len(self.trials) > 0 else None

        self.list_view = widgets.Output()
        with self.list_view:
            display(self.render_trails_list())

        self.detail_view = widgets.Output()
        with self.detail_view:
            display(self.render_trial())

        self.pagination_view = widgets.Output()
        with self.pagination_view:
            display(self.render_pagination())

    def load_detail(self, trial_button):
        trial_id = trial_button.tooltip
        trial = self.storage.get(trial_id)
        if isinstance(trial, Trial):
            self.selected_trial = trial
            with self.detail_view:
                clear_output()
                display(self.render_trial())
        else:
            raise Exception("Something went wrong during trial loading.")

    def render_trails_list(self):
        buttons = []
        for trial in self.trials:
            button = widgets.Button(
                description=f"{trial.name} | {trial.uuid}"[:30],
                disabled=False,
                button_style='',
                tooltip=trial.uuid,
                icon=''
            )
            button.layout = Layout(width="95%")
            button.on_click(self.load_detail)
            buttons.append(button)

        return widgets.VBox(buttons)

    def paginate(self, page_button):
        if page_button.tooltip == "prev":
            self.trials = self.storage.list(limit=self.limit, offset=self.offset - self.limit)
            self.offset = self.offset - self.limit
        elif page_button.tooltip == "next":
            self.trials = self.storage.list(limit=self.limit, offset=self.offset + self.limit)
            self.offset = self.offset + self.limit
        with self.list_view:
            clear_output()
            display(self.render_trails_list())
        with self.pagination_view:
            clear_output()
            display(self.render_pagination())

    def render_pagination(self):
        prev_page = widgets.Button(
            description='Prev',
            disabled=self.offset < 1,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='prev',
            icon='arrow-circle-left'  # (FontAwesome names without the `fa-` prefix)
        )
        prev_page.on_click(self.paginate)
        prev_page.layout = Layout(width="47%")

        next_page = widgets.Button(
            description='Next',
            disabled=len(self.trials) < 1,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='next',
            icon='arrow-circle-right'  # (FontAwesome names without the `fa-` prefix)
        )
        next_page.on_click(self.paginate)
        next_page.layout = Layout(width="47%")

        return widgets.HBox([prev_page, next_page])

    def search(self):
        search = widgets.Text(
            value='',
            placeholder='Name or description',
            description='Search:',
            disabled=False
        )
        search.layout = Layout(width="95%")
        return search

    def render_trial(self):
        tab_contents = ["Info", "Metrics", "Circuits", "Artifacts"]

        parameter_rows = [
            f"<tr><td>{name}</td><td>{value}</td></tr>"
            for name, value in self.selected_trial.parameters
        ]

        info = widgets.HTML(
            f"<h3>{self.selected_trial.name}</h3>"
            f"<h5>{self.selected_trial.uuid}</h5>"
            "<table border=2><tr><th>Parameter</th><th>Value</th></tr>"
            f"{parameter_rows}</table>")

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

        circuits = widgets.Output()
        with circuits:
            for name, circuit in self.selected_trial.circuits:
                print(name)
                print(circuit.draw(fold=-1))

        tab = widgets.Tab(children=[
            info,
            metrics,
            circuits
        ])
        tab.titles = ["Info", "Metrics", "Circuits"]

        return tab

    def show(self):
        grid = GridspecLayout(6, 3, height='400px')
        grid[:1, 1:] = self.search()
        grid[1:, 1:] = self.detail_view
        grid[:5, 0] = self.list_view
        grid[5:, 0] = self.pagination_view

        return grid
