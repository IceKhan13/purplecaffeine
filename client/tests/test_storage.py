"""Tests for Storage."""
import os
import shutil
from pathlib import Path
from unittest import TestCase
from testcontainers.compose import DockerCompose
from testcontainers.localstack import LocalStackContainer

from purplecaffeine.core import Trial, LocalStorage, S3Storage, ApiStorage
from purplecaffeine.exception import PurpleCaffeineException
from .test_trial import dummy_trial


class TestStorage(TestCase):
    """TestStorage."""

    def setUp(self) -> None:
        """SetUp Storage object."""
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(self.current_directory, "test_storage")
        if not os.path.exists(self.save_path):
            Path(self.save_path).mkdir(parents=True, exist_ok=True)
        self.local_storage = LocalStorage(path=self.save_path)
        self.my_trial = dummy_trial(name="keep_trial", storage=self.local_storage)

    def test_save_get_list_local_storage(self):
        """Test save trial locally."""
        # Save
        self.local_storage.save(trial=self.my_trial)
        self.assertTrue(
            os.path.isfile(os.path.join(self.save_path, f"{self.my_trial.uuid}.json"))
        )
        # Get
        recovered = self.local_storage.get(trial_id=self.my_trial.uuid)
        self.assertTrue(isinstance(recovered, Trial))
        self.assertEqual(recovered.parameters, [["test_parameter", "parameter"]])
        with self.assertRaises(ValueError):
            self.local_storage.get(trial_id="999")
        # List
        list_trials = self.local_storage.list(query="keep_trial")
        self.assertTrue(isinstance(list_trials, list))
        self.assertTrue(isinstance(list_trials[0], Trial))
        list_trials = self.local_storage.list(query="trial999")
        self.assertTrue(isinstance(list_trials, list))
        self.assertEqual(len(list_trials), 0)

    def test_save_get_api_storage(self):
        """Test save trial in API."""
        with DockerCompose(
            filepath=os.path.join(self.current_directory, "../.."),
            compose_file_name="docker-compose.yml",
            build=True,
        ) as compose:
            host = compose.get_service_host("api_server", 8000)
            port = compose.get_service_port("api_server", 8000)
            compose.wait_for(f"http://{host}:{port}/health_check/")

            storage = ApiStorage(
                host=f"http://{host}:{port}", username="admin", password="admin"
            )
            # Save
            storage.save(trial=self.my_trial)
            # Get
            recovered = storage.get(trial_id="1")
            self.assertTrue(isinstance(recovered, Trial))
            self.assertEqual(recovered.parameters, [["test_parameter", "parameter"]])
            with self.assertRaises(ValueError):
                storage.get(trial_id="999")

    def test_save_get_list_s3_storage(self) -> None:
        """Test of S3Storage object."""
        with LocalStackContainer(image="localstack/localstack:2.0.1") as localstack:
            localstack.with_services("s3")
            s3_storage = S3Storage(
                "bucket",
                access_key="",
                secret_access_key="",
                endpoint_url=localstack.get_url(),
            )
            s3_storage.client_s3.create_bucket(Bucket=s3_storage.bucket_name)

            # save
            uuid = s3_storage.save(trial=self.my_trial)
            # get
            recovered = s3_storage.get(trial_id=uuid)
            self.assertTrue(isinstance(recovered, Trial))
            with self.assertRaises(PurpleCaffeineException):
                s3_storage.get(trial_id="999")
            # list
            list_trials = s3_storage.list()
            self.assertTrue(isinstance(list_trials, list))
            for trial in list_trials:
                self.assertTrue(isinstance(trial, Trial))

    def tearDown(self) -> None:
        """TearDown Storage object."""
        file_to_remove = os.path.join(self.save_path)
        if os.path.exists(file_to_remove):
            shutil.rmtree(file_to_remove)
