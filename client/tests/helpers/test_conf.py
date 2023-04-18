"""Tests for Conf."""
from unittest import TestCase

from purplecaffeine.helpers import Configuration


class TestConf(TestCase):
    """TestConf."""

    def test_conf(self):
        """Test conf access variables."""
        self.assertTrue(isinstance(Configuration.MAX_SIZE, float))
        self.assertTrue(Configuration.MAX_SIZE > 1000000)
