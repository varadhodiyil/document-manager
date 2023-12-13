from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin

from rest_framework.viewsets import GenericViewSet

from propylon_document_manager.file_versions.models import FileVersion, Files
from .serializers import FileVersionSerializer, FilesSerializer
from propylon_document_manager.file_versions.permissions import IsFileOwner
from propylon_document_manager.file_versions.models import FileVersion


class FilesViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsFileOwner]
    queryset = Files.objects.all()
    lookup_field = "id"
    serializer_class = FilesSerializer

    def perform_create(self, serializer):
        file = serializer.save()
        fv_serializer = FileVersionSerializer(data={"file": file.id, "version_number": 1})
        fv_serializer.is_valid(raise_exception=True)
        fv_serializer.save()


class FileVersionViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsFileOwner]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"

    def perform_create(self, serializer) -> None:
        file = serializer.validated_data["file"]
        print(file.__dict__)
        new_version = file.current_version + 1
        serializer.validated_data["version_number"] = new_version

        serializer.save()
        file.save()
