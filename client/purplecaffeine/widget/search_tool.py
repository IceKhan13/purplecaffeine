from purplecaffeine.core import LocalStorage, Trial, BaseStorage
from IPython.display import display, clear_output
import ipywidgets as widgets

class Search_tool:
    def __init__(self):
        self.search = widgets.Text(
            value='',
            placeholder='Name or description',
            description='',
            disabled=False
        )
        self.search_button = widgets.Button(
            description='Search',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='search',
            icon=''  # (FontAwesome names without the `fa-` prefix)
        )

    def display_search_button(self):
        search_button = widgets.Button(
            description='Search',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='search',
            icon=''  # (FontAwesome names without the `fa-` prefix)
        )
        search_button.on_click(search_function)
        search_button.add_class('btn')
        search_button.add_class('btn-secondary')


    def search_function(self, search_button):
        self.limit = 10
        self.offset = 0
        if(search.value == ''):
            self.trials = self.storage.list(limit=self.limit, offset=self.offset)
        else:
            self.trials = list(filter(lambda trial: search.value in trial.name, self.storage.get_all()))
        with self.list_view:
            clear_output()
            display(self.render_trails_list())
        with self.detail_view:
            clear_output()
            if(len(self.trials) > 0):
                self.selected_trial = self.trials[0]
                display(self.render_trial())
        with self.pagination_view:
            clear_output()
            display(self.render_pagination())