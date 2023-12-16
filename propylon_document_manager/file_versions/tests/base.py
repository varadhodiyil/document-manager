# pylint: disable=W0201
import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory

from propylon_document_manager.file_versions.models import Files
from propylon_document_manager.users.tests.factories import Faker, UserFactory


class TestFileVersions:
    @pytest.fixture
    def api_rf(self) -> RequestFactory:
        return APIRequestFactory()

    def setup_method(self, method):  # noqa
        self.user = UserFactory()
        self.second_user = UserFactory()

        self.user_file = Files.objects.create(
            file_name="file_1.ext", user=self.user, file_url="/documents/test-1/test.ext"
        )
        self.second_user_file = Files.objects.create(
            file_name="file_2.ext", user=self.second_user, file_url="/documents/test-1/test.ext"
        )
