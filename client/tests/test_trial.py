"""Tests for Trial."""

from unittest import TestCase

from purplecaffeine.trail import Trial


class TestTrial(TestCase):
    """TestTrial."""

    def test_trail_context(self):
        """Test train context."""
        with Trial("test_trial") as trial:
            trial.add_metric("some_metric", 1)
