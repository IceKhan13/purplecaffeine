"""Widget."""
from typing import List, Optional

import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, clear_output
from ipywidgets import Layout, GridspecLayout, AppLayout
from purplecaffeine.core import BaseStorage, LocalStorage, Trial


class Widget:
    """Widget class.

    Attributes:
        storage (BaseStorage): storage where the trials are going to be saved
        limit (int): number of trials per page
        offset (int): aux int to paginate result
        current_page_trials (List[Trial]): list of trials
        next_page_trials (List[Trial]): list of trials for next page
        selected_trial (Trial): current trial on display
         (List[(str, Any)]): list of artifact, any external files
        search_value (str): value that the user puts on search bar
        list_view (DomWidget): widget to display list of trials
        detail_view (DomWidget): widget to display the details of a trial
        pagination_view (DomWidget): widget to display the pagination buttons
    """

    def __init__(self, storage: Optional[BaseStorage] = None):
        """Widget class:
        Attributes:
            storage (BaseStorage): storage where the trials are going to be saved
        """
        self.storage = storage or LocalStorage("./trials")
        self.limit = 10
        self.offset = 0
        self.current_page_trials: List[Trial] = self.storage.list(
            limit=self.limit, offset=self.offset
        )
        self.next_page_trials: List[Trial] = self.storage.list(
            limit=self.offset + self.limit + self.limit, offset=self.offset + self.limit
        )
        self.selected_trial: Optional[Trial] = (
            self.current_page_trials[0] if len(self.current_page_trials) > 0 else None
        )
        self.search_value = ""

        self.list_view = widgets.Output()
        with self.list_view:
            display(self.render_trails_list())

        self.detail_view = widgets.Output()
        with self.detail_view:
            display(self.render_trial())

        self.pagination_view = widgets.Output()
        with self.pagination_view:
            display(self.render_pagination())

    def display_message(self, required_message):
        """
        Returns a user-friendly message for displaying
        Returns:
            empty_message (HTMLWidget): the widget with the info
        """
        empty_message = widgets.HTML(
            f"<h1 style='text-align: center;'> <br><br><br>{required_message}</h1>"
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/'
            'dist/css/bootstrap.min.css" '
            'integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" '
            'crossorigin="anonymous">'
        )
        empty_message.layout = Layout(height="300px")
        return empty_message

    def load_detail(self, trial_button):
        """
        Load the details of a trial
            Args:
            trial_button: a trial button that was clicked
        """
        trial_id = trial_button.tooltip
        trial = self.storage.get(trial_id)
        if isinstance(trial, Trial):
            self.selected_trial = trial
            with self.detail_view:
                clear_output()
                display(self.render_trial())
        else:
            self.display_message("Something went wrong while loading your trials ):")

    def render_trails_list(self):
        """
        Render the list of trail buttons.
        We render one button per each trial
        """
        buttons = []
        for trial in self.current_page_trials:
            button = widgets.Button(
                description=f"{trial.name} | {trial.uuid}"[:30],
                disabled=False,
                button_style="",
                tooltip=trial.uuid,
                icon="",
            )
            button.layout = Layout(width="95%")
            button.on_click(self.load_detail)
            buttons.append(button)

        return widgets.VBox(buttons)

    def paginate(self, page_button):
        """
        Displays the pagination accordingly to the clicked button
        and the list of trials for the current
        page.
        Args:
            page_button (WidgetButton): clicked pagination button
        """
        if page_button.tooltip == "prev":
            self.next_page_trials = self.current_page_trials
            self.current_page_trials = self.storage.list(
                limit=self.limit,
                offset=self.offset - self.limit,
                query=self.search_value,
            )
            self.offset = self.offset - self.limit
        elif page_button.tooltip == "next":
            self.current_page_trials = self.next_page_trials
            self.offset = self.offset + self.limit
            self.next_page_trials = self.storage.list(
                limit=self.offset + self.limit,
                offset=self.offset + self.limit,
                query=self.search_value,
            )
        with self.list_view:
            clear_output()
            display(self.render_trails_list())
        with self.pagination_view:
            clear_output()
            display(self.render_pagination())

    def render_pagination(self):
        """
        Displays the pagination buttons
        and the list of trials for the current
        page.
        """
        prev_page = widgets.Button(
            description="Prev",
            disabled=self.offset < 1,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="prev",
            icon="arrow-circle-left",  # (FontAwesome names without the `fa-` prefix)
        )
        prev_page.on_click(self.paginate)
        prev_page.layout = Layout(width="47%")
        prev_page.add_class("btn")
        prev_page.add_class("btn-secondary")
        next_page = widgets.Button(
            description="Next",
            disabled=len(self.next_page_trials) == 0,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="next",
            icon="arrow-circle-right",  # (FontAwesome names without the `fa-` prefix)
        )
        next_page.add_class("btn")
        next_page.add_class("btn-secondary")
        next_page.on_click(self.paginate)
        next_page.layout = Layout(width="47%")

        return widgets.HBox([prev_page, next_page])

    def search(self):
        """
        Displays the search bar and button.
        """
        search = widgets.Text(
            value="", placeholder="Name or description", description="", disabled=False
        )
        search_button = widgets.Button(
            description="Search",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="search",
            icon="",  # (FontAwesome names without the `fa-` prefix)
        )

        def search_function(clicked_button):
            """
            Function that filters the trial list
            accordingly to the
            input received from user.
            """
            # pylint: disable=unused-argument
            self.search_value = search.value
            self.limit = 10
            self.offset = 0
            if search.value == "":
                self.current_page_trials = self.storage.list(
                    limit=self.limit, offset=self.offset, query=self.search_value
                )
                self.next_page_trials = self.storage.list(
                    limit=self.offset + self.limit + self.limit,
                    offset=self.offset + self.limit,
                    query=self.search_value,
                )
            else:
                self.current_page_trials = self.storage.list(
                    limit=self.limit, offset=self.offset, query=search.value
                )
                self.next_page_trials = self.storage.list(
                    limit=self.offset + self.limit + self.limit,
                    offset=self.offset + self.limit,
                    query=self.search_value,
                )
            with self.list_view:
                clear_output()
                display(self.render_trails_list())
            with self.detail_view:
                clear_output()
                if len(self.current_page_trials) > 0:
                    self.selected_trial = self.current_page_trials[0]
                    display(self.render_trial())
            with self.pagination_view:
                clear_output()
                display(self.render_pagination())

        search.layout = Layout(width="99%")
        search_button.on_click(search_function)
        search_button.add_class("btn")
        search_button.add_class("btn-secondary")

        return AppLayout(
            header=None,
            left_sidebar=search_button,
            center=None,
            right_sidebar=search,
            footer=None,
            pane_widths=[1, 0, 5],
        )

    def render_trial(self):
        """
        Load the tabs with the basic info, circuits and metrics
        of the selected trial
        """
        if self.selected_trial is None:
            return self.display_message("Add a new trial to see the info of that trial")

        parameter_rows = "".join(
            [
                f"<tr><td>{str(name)}</td><td><button class='btn btn-primary "
                f"rounded-pill' disabled>{str(value)}</button"
                f"></td></tr>"
                for name, value in self.selected_trial.parameters
            ]
        )

        tags = "".join(
            [
                f"<button class='btn btn-primary rounded-pill btn-sm' "
                f"style='margin-bottom:20px; margin-right: 10px' "
                f"disabled>{str(tag)}</button>"
                for tag in self.selected_trial.tags
            ]
        )

        info = widgets.HTML(
            f"<h3>{self.selected_trial.name} | {self.selected_trial.uuid} </h3>"
            f"<p>Description: {self.selected_trial.description}</p>"
            f"<div>{tags}</div>"
            "<table border=2 class='table'><tr><th>Parameter</th><th>Value</th></tr>"
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/'
            'bootstrap@5.2.3/dist/css/bootstrap.min.css" '
            'integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" '
            'crossorigin="anonymous">'
            f"{parameter_rows}</table>"
        )
        info.layout = Layout(overflow="scroll", max_height="300px")
        metrics = widgets.Output()
        with metrics:
            data_frame = pd.DataFrame(
                self.selected_trial.metrics, columns=["name", "value"]
            )
            df2 = data_frame.groupby("name").agg(list)
            for metric_name, values in df2.to_dict()["value"].items():
                if len(values) == 1:
                    pass
                else:
                    plt.plot(values)
                    plt.xlabel("entry")
                    plt.ylabel("value")
                    plt.title(f"Metric: {metric_name}")
                    plt.show()
        metrics.layout = Layout(overflow="scroll", max_height="300px")
        circuits = widgets.Output()
        with circuits:
            for name, circuit in self.selected_trial.circuits:
                print(name)
                print(circuit)
        circuits.layout = Layout(overflow="scroll", max_height="300px")

        tab = widgets.Tab(children=[info, metrics, circuits])
        tab.titles = ["Info", "Metrics", "Circuits"]

        return tab

    def show(self):
        """
        Function to assemble all the other
        widgets into one
        """
        grid = GridspecLayout(2, 1, height="500px")
        grid[0, 0] = self.list_view
        grid[1, 0] = self.pagination_view

        return AppLayout(
            header=self.search(),
            left_sidebar=grid,
            center=self.detail_view,
            right_sidebar=None,
            footer=None,
            pane_widths=[0.5, 1, 1],
            pane_heights=[0.5, 5, 1],
        )
