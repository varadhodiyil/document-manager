# pylint: disable=W0201
import json
import tempfile
from hashlib import sha1

import pytest
from django.core.files.base import ContentFile
from rest_framework.test import APIRequestFactory

from propylon_document_manager.file_versions.api.utils import generate_hash
from propylon_document_manager.file_versions.api.views import FilesViewSet, FileVersionViewSet
from propylon_document_manager.file_versions.models import FileVersion
from propylon_document_manager.file_versions.tests.base import TestFileVersions


def _gen_content(version: int) -> str:
    return f"Version {version}"


def make_file(version: int) -> ContentFile:
    return ContentFile(_gen_content(version))


@pytest.mark.django_db
class TestUserViewSet(TestFileVersions):
    def setup_method(self, method):
        super().setup_method(method)

        self.user_file_version_1 = FileVersion.objects.create(
            file=self.user_file, version_number=1, uploaded_file=make_file(1), file_hash=generate_hash(make_file(1))
        )
        self.user_file_version_2 = FileVersion.objects.create(
            file=self.user_file, version_number=2, uploaded_file=make_file(2), file_hash=generate_hash(make_file(2))
        )
        self.user_file.current_version = 2
        self.user_file.save()

        self.second_user_file_version_1 = FileVersion.objects.create(
            file=self.second_user_file,
            version_number=1,
            uploaded_file=make_file(1),
            file_hash=generate_hash(make_file(1)),
        )
        self.second_user_file_version_2 = FileVersion.objects.create(
            file=self.second_user_file,
            version_number=2,
            uploaded_file=make_file(2),
            file_hash=generate_hash(make_file(2)),
        )
        self.second_user_file.current_version = 2
        self.second_user_file.save()

    @pytest.mark.django_db
    @pytest.mark.django_db
    def test_get_all_file_versions_user(self, api_rf: APIRequestFactory):
        """Test List all File versions"""

        view = FilesViewSet.as_view({"get": "list"})
        request = api_rf.get("/file_versions/")
        request.user = self.user

        view.request = request
        response = view(request).render()

        response_data = json.loads(response.content)
        assert response.status_code == 200
        assert response_data == [
            {
                "added_at": self.user_file.added_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": self.user_file.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "id": 1,
                "versions": [
                    {
                        "id": self.user_file_version_1.id,
                        "version_number": self.user_file_version_1.version_number,
                        "added_at": self.user_file_version_1.added_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "updated_at": self.user_file_version_1.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "file": self.user_file.id,
                        "uploaded_file": self.user_file_version_1.uploaded_file,
                    },
                    {
                        "id": self.user_file_version_2.id,
                        "version_number": self.user_file_version_2.version_number,
                        "added_at": self.user_file_version_2.added_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "updated_at": self.user_file_version_2.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "file": self.user_file.id,
                        "uploaded_file": self.user_file_version_2.uploaded_file,
                    },
                ],
                "current_version": 2,
                "file_url": self.user_file.file_url,
                "file_name": self.user_file.file_name,
            }
        ]

        for res in response_data:
            assert res["id"] != self.second_user_file.id
            for ver in res["versions"]:
                assert ver["file"] == self.user_file.id
                assert ver["id"] not in (self.second_user_file_version_1.id, self.second_user_file_version_2.id)

    @pytest.mark.django_db
    def test_get_file_version_user(self, api_rf: APIRequestFactory):
        """Get Individual File, Authenticated User"""
        view = FileVersionViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/file_versions")
        request.user = self.user

        view.request = request
        response = view(request, id=self.user_file_version_1.id).render()

        response_data = json.loads(response.content)
        assert response.status_code == 200
        assert response_data == {
            "added_at": self.user_file_version_1.added_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": self.user_file_version_1.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "id": self.user_file_version_1.id,
            "version_number": self.user_file_version_1.version_number,
            "file": self.user_file.id,
            "uploaded_file": None,
        }

        assert response_data["id"] == self.user_file.id

    @pytest.mark.django_db
    def test_delete_version_user(self, api_rf: APIRequestFactory):
        """Get Individual File, Authenticated User"""
        view = FileVersionViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/file_versions")
        request.user = self.user

        view.request = request
        response = view(request, id=self.user_file_version_1.id).render()

        assert response.status_code == 204

        # Test Get After Delete
        view = FileVersionViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/file_versions")
        request.user = self.user

        view.request = request
        response = view(request, id=self.user_file_version_1.id).render()

        assert response.status_code == 404

    @pytest.mark.django_db
    def test_delete_current_version_user(self, api_rf: APIRequestFactory):
        """Get Individual File, Authenticated User"""
        view = FileVersionViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/file_versions")
        request.user = self.user

        view.request = request
        response = view(request, id=self.user_file_version_2.id).render()

        assert response.status_code == 204

    @pytest.mark.django_db
    def test_create_new_file_version_user(self, api_rf: APIRequestFactory):
        """Create Files"""
        view = FileVersionViewSet.as_view({"post": "create"})
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test version2")
            tmp.close()
            with open(tmp.name, "rb") as test_file:
                request = api_rf.post(
                    "/file_versions/",
                    {"uploaded_file": test_file, "file": self.second_user_file.id},
                    format="multipart",
                )
                request.user = self.user

                view.request = request
                response = view(request, id=self.second_user_file.id).render()

                response_data = json.loads(response.content)

                assert response.status_code == 201
                assert response_data["id"] == 5
                assert response_data["version_number"] == self.second_user_file.current_version + 1

    @pytest.mark.django_db
    def test_create_new_file_same_content_version_user(self, api_rf: APIRequestFactory):
        """Create File Version with Same content"""
        view = FileVersionViewSet.as_view({"post": "create"})

        request = api_rf.post(
            "/file_versions/",
            {"uploaded_file": make_file(1), "file": self.second_user_file.id},
            format="multipart",
        )
        request.user = self.user

        view.request = request
        response = view(request, id=self.second_user_file.id).render()

        response_data = json.loads(response.content)

        assert response.status_code == 400
        assert response_data == {"non_field_errors": ["File Version already exits"]}
