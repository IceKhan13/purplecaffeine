#!/usr/bin/env python
# coding: utf-8

# Copyright (c) purplecaffeine.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..widget import Widget

def test_example_creation_blank():
    w = Widget()
    assert w.value == 'Hello World'
