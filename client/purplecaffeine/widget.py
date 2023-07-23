"""Widget."""
from typing import List, Optional

import ipywidgets as widgets
import pandas as pd
from IPython.display import display, clear_output
from ipywidgets import Layout, GridspecLayout, AppLayout
from matplotlib import pyplot as plt

from purplecaffeine.core import BaseStorage, LocalStorage, Trial


def display_message(required_message):
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


TABLE_STYLE = """
<style>
    table {
        width: 100% !important;
        font-family:IBM Plex Sans, Arial, sans-serif !important;
    }

    th, td {
        text-align: left !important;
        padding: 5px !important;
    }

    tr:nth-child(even) {background-color: #f6f6f6 !important;}
</style>
"""


class Widget:
    """Widget class.

    Attributes:
        storage (BaseStorage): storage where the trials are going to be saved
        limit (int): number of trials per page
        offset (int): aux int to paginate result
        trials (List[Trial]): list of trials
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
        self.trials: List[Trial] = self.storage.list(
            limit=self.limit, offset=self.offset
        )
        self.selected_trial: Optional[Trial] = (
            self.trials[0] if len(self.trials) > 0 else None
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
            display_message("Something went wrong while loading your trials ):")

    def render_trails_list(self):
        """
        Render the list of trail buttons.
        We render one button per each trial
        """
        buttons = []
        for trial in self.trials:
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

    def render_pagination(self):
        """
        Displays the pagination buttons
        and the list of trials for the current
        page.
        """

        def paginate(page_button):
            """
            Displays the pagination accordingly to the clicked button
            and the list of trials for the current
            page.
            Args:
                page_button (WidgetButton): clicked pagination button
            """
            if page_button.tooltip == "prev":
                self.offset = self.offset - self.limit
                self.trials = self.storage.list(
                    limit=self.limit,
                    offset=self.offset,
                    query=self.search_value,
                )
            elif page_button.tooltip == "next":
                self.offset = self.offset + self.limit
                self.trials = self.storage.list(
                    limit=self.limit,
                    offset=self.offset,
                    query=self.search_value,
                )

            print(self.offset, self.limit)

            with self.list_view:
                clear_output()
                display(self.render_trails_list())
            with self.pagination_view:
                clear_output()
                display(self.render_pagination())

        prev_page = widgets.Button(
            description="Prev",
            disabled=self.offset < 1,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="prev",
            icon="arrow-circle-left",  # (FontAwesome names without the `fa-` prefix)
        )
        prev_page.on_click(paginate)
        prev_page.layout = Layout(width="47%")
        next_page = widgets.Button(
            description="Next",
            disabled=len(self.trials) < self.limit,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="next",
            icon="arrow-circle-right",  # (FontAwesome names without the `fa-` prefix)
        )
        next_page.on_click(paginate)
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
            self.trials = self.storage.list(
                limit=self.limit, offset=self.offset, query=self.search_value
            )
            with self.list_view:
                clear_output()
                display(self.render_trails_list())
            with self.detail_view:
                clear_output()
                if len(self.trials) > 0:
                    self.selected_trial = self.trials[0]
                    display(self.render_trial())
            with self.pagination_view:
                clear_output()
                display(self.render_pagination())

        search.layout = Layout(width="99%")
        search_button.on_click(search_function)

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
            return display_message("Add a new trial to see the info of that trial")

        def render_table(entries):
            """
            Method to construct a new html string representing
            a table using name and values.

            Returns:
                table string (str): html string that contains the table
            """
            if len(entries) == 0:
                return ""

            rows = [
                f"""
                <tr>
                    <td>{key}</td>
                    <td>{value}</td>
                </tr>
                """
                for key, value in entries
            ]

            return f"""
                <table>
                    {TABLE_STYLE}
                    <tr>
                        <th>Key</th>
                        <th>Value</th>
                    </tr>
                    {"".join(rows)}
                </table>
            """

        def render_line_plot(title, values):
            """Renders line plot."""
            plt.plot(values)
            plt.xlabel("entry")
            plt.ylabel("value")
            plt.title(f"Metric: {title}")
            plt.show()

        # info tab
        info_html = f"""
            <b>{self.selected_trial.name}</b> #{self.selected_trial.uuid}
            <div>{" ".join([
                f"<span style='color:blue'>#{tag}</span>"
                for tag in self.selected_trial.tags
            ])}</div>
            <p>Description: {self.selected_trial.description or "..."}</p>
            {render_table(self.selected_trial.parameters)}
        """
        info_tab = widgets.HTML(info_html)
        info_tab.layout = Layout(overflow="scroll", max_height="300px")

        # metrics tab
        metrics_tab = widgets.Output()
        metrics_tab.layout = Layout(overflow="scroll", max_height="500px")
        with metrics_tab:
            dataframe = (
                pd.DataFrame(self.selected_trial.metrics, columns=["name", "value"])
                .groupby("name")
                .agg(list)
            )
            metrics_to_table = []
            metrics_to_plot = []
            for metric_name, values in dataframe.to_dict()["value"].items():
                if len(values) == 1:
                    metrics_to_table.append((metric_name, values[0]))
                else:
                    metrics_to_table.append((metric_name, values))
                    metrics_to_plot.append((metric_name, values))
            metrics_html = widgets.HTML(
                f"""
                <div>
                    <b>Metrics</b>
                    {render_table(metrics_to_table)}
                </div>
            """
            )
            display(metrics_html)

            for metric_name, values in metrics_to_plot:
                render_line_plot(metric_name, values)

        # circuits tab
        circuits_tab = widgets.Output()
        with circuits_tab:
            display(widgets.HTML("<div> <b>Circuits</b></div>"))
            for name, circuit in self.selected_trial.circuits:
                axis = plt.subplot(111)
                axis.set_title(name)
                circuit.draw("mpl", ax=axis)
                plt.show()

        circuits_tab.layout = Layout(overflow="scroll", max_height="500px")

        # texts tab
        texts_html = f"""
            <div>
                <b>Texts</b>
            </div>
            {render_table(self.selected_trial.texts)}
        """
        texts_tab = widgets.HTML(texts_html)
        texts_tab.layout = Layout(overflow="scroll", max_height="300px")

        # operators tab
        operators_html = f"""
            <div>
                <b>Operators</b>
            </div>
            {render_table(self.selected_trial.operators)}
        """
        operators_tab = widgets.HTML(operators_html)
        operators_tab.layout = Layout(overflow="scroll", max_height="300px")

        tab = widgets.Tab(
            children=[info_tab, metrics_tab, circuits_tab, operators_tab, texts_tab]
        )
        tab.titles = ["Info", "Metrics", "Circuits", "Operators", "Texts"]
        return tab

    def show(self):
        """
        Function to assemble all the other
        widgets into one
        """
        grid = GridspecLayout(10, 3)
        grid[0, :] = self.search()
        grid[1:8, 0:1] = self.list_view
        grid[1:9, 1:] = self.detail_view
        grid[8, :1] = self.pagination_view
        return grid
