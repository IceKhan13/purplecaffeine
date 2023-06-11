"""Tests for Trial."""
import os
from pathlib import Path
from unittest import TestCase

from purplecaffeine.core import LocalStorage
from purplecaffeine.widget import Widget


class TestWidget(TestCase):
    """TestTrial."""

    def setUp(self) -> None:
        """SetUp local storage backend for widget use"""
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(curr_dir, "test")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_storage = LocalStorage(path=self.save_path)

    def test_empty_string(self):
        widget = Widget(self.local_storage)
        """Test when we don't have trials."""
        self.assertEqual(widget.display_empty().value,
                         "<h1 style='text-align: center;'> <br><br><br>Add a new trial "
                         "to see the"
                         "info of that trial </h1>"
                         '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/'
                         'bootstrap@5.2.3/dist/'
                         'css/bootstrap.min.css" '
                         'integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW'
                         '1RWuH61DGLwZJEdK2Kadq2F9CUG65" '
                         'crossorigin="anonymous">')
