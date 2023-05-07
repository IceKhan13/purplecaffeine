"""Tests for Conf."""
from unittest import TestCase

from purplecaffeine.helpers import Configuration


class TestConf(TestCase):
    """TestConf."""

    def test_conf(self):
        """Test conf access variables."""
        self.assertTrue(isinstance(Configuration.MAX_SIZE, float))
        self.assertTrue(Configuration.MAX_SIZE > 1000000)
        self.assertTrue(Configuration.API_HTTP == "http")
        self.assertTrue(Configuration.API_URL == "127.0.0.1")
        self.assertTrue(Configuration.API_PORT == "8000")
        self.assertTrue(Configuration.API_TRIAL_ENDPOINT == "api/trials")
        self.assertTrue(
            Configuration.API_FULL_URL == "http://127.0.0.1:8000/api/trials"
        )
        self.assertTrue(
            Configuration.API_HEADERS
            == {"Accept": "application/json", "Content-Type": "application/json"}
        )
        self.assertTrue(Configuration.API_TIMEOUT == 30)

        self.assertTrue(isinstance(Configuration.all(), list))
