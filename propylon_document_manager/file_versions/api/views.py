from typing import Any
import os
from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from propylon_document_manager.file_versions.api.serializers import FilesSerializer, FileVersionSerializer
from propylon_document_manager.file_versions.models import Files, FileVersion
from propylon_document_manager.file_versions.permissions import IsFileOwner
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from django.http import FileResponse
from django.shortcuts import get_object_or_404


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
        fv_serializer = FileVersionSerializer(data={"file": file.id, "uploaded_file": uploaded_file})
        fv_serializer.is_valid(raise_exception=True)

        fv_serializer.save(version_number=file.current_version)

    def perform_update(self, serializer) -> None:
        uploaded_file = serializer.validated_data.pop("uploaded_file")
        fv_serializer = FileVersionSerializer(data={"file": serializer.instance.id, "uploaded_file": uploaded_file})
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

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        lookups = Q(file__user=self.request.user)
        return self.queryset.filter(lookups)

    def perform_create(self, serializer) -> None:
        file = serializer.validated_data["file"]

        new_version = file.current_version + 1
        serializer.validated_data["version_number"] = new_version
        file.current_version = new_version
        serializer.save()
        file.save()

    def perform_destroy(self, instance: FileVersion) -> None:
        if instance.file.current_version == instance.version_number:
            instance.file.current_version = instance.file.current_version - 1
            instance.file.save()
        instance.delete()

        if instance.file.current_version == 0:
            instance.file.delete()


class DownloadView(GenericAPIView):
    permission_classes = [IsFileOwner]
    serializer_class = FileVersionSerializer
    queryset = Files.objects.all()

    def get_queryset(self) -> QuerySet[Any]:
        base = self.request.path
        return Files.objects.filter(file_url=base, user=self.request.user)

    def get(self, request):
        qs = self.get_queryset()
        if not qs:
            return Response({"status": False}, status=HTTP_403_FORBIDDEN)
        file_model = qs.get()
        version = request.GET.get("revision", file_model.current_version)
        file_version = get_object_or_404(FileVersion.objects.filter(file=file_model, version_number=version))

        media_file = os.path.join(settings.MEDIA_ROOT, file_version.uploaded_file.name)
        file = open(media_file, "rb")
        return FileResponse(file, as_attachment=True, filename=os.path.basename(media_file))
