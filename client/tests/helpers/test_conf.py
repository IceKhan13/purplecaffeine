"""Tests for Conf."""
from unittest import TestCase

from purplecaffeine.helpers import Configuration


class TestConf(TestCase):
    """TestConf."""

    def test_conf(self):
        """Test conf access variables."""
        self.assertTrue(isinstance(Configuration.MAX_SIZE, float))
        self.assertTrue(Configuration.MAX_SIZE > 1000000)
        self.assertTrue(Configuration.API_TRIAL_ENDPOINT == "api/trials")
        self.assertTrue(Configuration.API_TOKEN_ENDPOINT == "api/token")
        self.assertTrue(
            Configuration.API_HEADERS
            == {"Accept": "application/json", "Content-Type": "application/json"}
        )
        self.assertTrue(Configuration.API_TIMEOUT == 30)

        self.assertTrue(isinstance(Configuration.all(), list))
