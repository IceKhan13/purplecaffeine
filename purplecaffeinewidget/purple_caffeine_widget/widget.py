#!/usr/bin/env python
# coding: utf-8

# Copyright (c) purplecaffeine.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget, ValueWidget
from traitlets import List, Unicode
from ._frontend import module_name, module_version

from purplecaffeine.core import Trial, LocalBackend


class Widget(DOMWidget, ValueWidget):

    """TODO: Add docstring here"""
    _model_name = Unicode('WidgetModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('WidgetView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    local_backend = LocalBackend("./")

    my_list = [x.name for x in local_backend.list()]

    value = List(my_list).tag(sync=True)
