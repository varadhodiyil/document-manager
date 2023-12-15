from django.db.models.query import QuerySet
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)


from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from propylon_document_manager.file_versions.models import FileVersion, Files
from propylon_document_manager.file_versions.api.serializers import FileVersionSerializer, FilesSerializer
from propylon_document_manager.file_versions.permissions import IsFileOwner
from propylon_document_manager.file_versions.models import FileVersion


class FilesViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet, DestroyModelMixin
):
    permission_classes = [IsFileOwner]
    queryset = Files.objects.all()
    lookup_field = "id"
    serializer_class = FilesSerializer

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        lookups = Q(user=self.request.user)
        return self.queryset.filter(lookups)

    def perform_create(self, serializer):
        uploaded_file = serializer.validated_data.pop("uploaded_file")

        file = serializer.save(file_name=uploaded_file.name)
        fv_serializer = FileVersionSerializer(data={"file": file.id})
        fv_serializer.is_valid(raise_exception=True)
        fv_serializer.save(version_number=1)

    def perform_update(self, serializer) -> None:
        uploaded_file = serializer.validated_data.pop("uploaded_file")
        fv_serializer = FileVersionSerializer(data={"file": serializer.instance.id})
        fv_serializer.is_valid(raise_exception=True)
        new_version = serializer.instance.current_version + 1
        fv_serializer.save(version_number=new_version)
        serializer.instance.current_version = new_version
        serializer.save(file_name=uploaded_file.name)


class FileVersionViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet, DestroyModelMixin):
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

    def perform_destroy(self, instance: FileVersion) -> None:
        if instance.file.current_version == instance.version_number:
            instance.file.current_version = instance.file.current_version - 1
            instance.file.save()
        instance.delete()
