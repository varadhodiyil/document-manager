from typing import Any
from rest_framework import serializers

from propylon_document_manager.file_versions.models import FileVersion, Files


class FileVersionSerializer(serializers.ModelSerializer):
    version_number = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = FileVersion
        fields = "__all__"


class FilesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    versions = FileVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Files
        fields = ["file_name", "added_at", "updated_at", "id", "user", "versions"]
