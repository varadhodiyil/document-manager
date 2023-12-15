import json
import tempfile

import pytest
from rest_framework.test import APIRequestFactory

from propylon_document_manager.file_versions.api.views import FilesViewSet
from propylon_document_manager.file_versions.tests.base import TestFileVersions


@pytest.mark.django_db
class TestUserViewSet(TestFileVersions):
    @pytest.mark.django_db
    def test_get_all_files_user(self, api_rf: APIRequestFactory):
        """Test List all Files"""
        view = FilesViewSet.as_view({"get": "list"})
        request = api_rf.get("/files/")
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
                "versions": [],
                "current_version": 1,
            }
        ]
        for res in response_data:
            assert res["id"] != self.second_user_file.id

    @pytest.mark.django_db
    def test_get_file_user(self, api_rf: APIRequestFactory):
        """Get Individual File, Authenticated User"""
        view = FilesViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/files")
        request.user = self.user

        view.request = request
        response = view(request, id=self.user_file.id).render()

        response_data = json.loads(response.content)
        assert response.status_code == 200
        assert response_data == {
            "added_at": self.user_file.added_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": self.user_file.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "id": 1,
            "versions": [],
            "current_version": 1,
        }

        assert response_data["id"] == self.user_file.id

    @pytest.mark.django_db
    def test_get_file_user_invalid_user(self, api_rf: APIRequestFactory):
        """Get Individual File, Invalid User"""
        view = FilesViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/files")
        request.user = self.user

        view.request = request
        response = view(request, id=self.second_user_file.id).render()

        response_data = json.loads(response.content)
        assert response.status_code == 404
        assert response_data == {"detail": "Not found."}

    @pytest.mark.django_db
    def test_create_new_file_user(self, api_rf: APIRequestFactory):
        """Create Files"""
        view = FilesViewSet.as_view({"post": "create"})
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Version 1")
            tmp.close()
            with open(tmp.name, "rb") as test_file:
                request = api_rf.post(
                    "/files/",
                    {"uploaded_file": test_file},
                    format="multipart",
                )
                request.user = self.user

                view.request = request
                response = view(request).render()

                response_data = json.loads(response.content)
                assert response.status_code == 201
                assert response_data["id"] == 3
                assert response_data["current_version"] == 1
                new_file_id = response_data["id"]
        # Test Get After Create
        view = FilesViewSet.as_view({"get": "list"})
        request = api_rf.get("/files/")
        request.user = self.user

        view.request = request
        response = view(request).render()

        response_data = json.loads(response.content)
        assert response.status_code == 200
        assert len(response_data) == 2
        assert response_data[len(response_data) - 1]["id"] == new_file_id

        for res in response_data:
            assert res["id"] != self.second_user_file.id

    @pytest.mark.django_db
    def test_delete_user(self, api_rf: APIRequestFactory):
        """Delete User File"""
        view = FilesViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/files")
        request.user = self.user

        view.request = request
        response = view(request, id=self.user_file.id).render()

        assert response.status_code == 204

        # Test Get After Delete

        view = FilesViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/files")
        request.user = self.user

        view.request = request
        response = view(request, id=self.user.id).render()

        response_data = json.loads(response.content)
        assert response.status_code == 404
        assert response_data == {"detail": "Not found."}

    @pytest.mark.django_db
    def test_delete_user_invalid_user(self, api_rf: APIRequestFactory):
        """Delete Incorrect User File"""
        view = FilesViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/files")
        request.user = self.second_user

        view.request = request
        response = view(request, id=self.user_file.id).render()

        assert response.status_code == 404

    @pytest.mark.django_db
    def test_update_file_user(self, api_rf: APIRequestFactory):
        """Create Files"""
        view = FilesViewSet.as_view({"put": "update"})
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Version 2")
            tmp.close()
            with open(tmp.name, "rb") as test_file:
                request = api_rf.put(
                    "/files/",
                    {"uploaded_file": test_file},
                    format="multipart",
                )
                request.user = self.user

                view.request = request
                response = view(request, id=self.user_file.id).render()

                response_data = json.loads(response.content)

                assert response.status_code == 200
                assert response_data["id"] == self.user_file.id
                assert response_data["current_version"] == self.user_file.current_version + 1
