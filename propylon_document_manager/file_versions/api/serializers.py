from typing import Any
from rest_framework import serializers

from propylon_document_manager.file_versions.models import Files, FileVersion


class FileVersionSerializer(serializers.ModelSerializer):
    version_number = serializers.ReadOnlyField(read_only=True)
    uploaded_file = serializers.FileField(write_only=True)

    def create(self, validated_data: Any) -> Any:
        uploaded_file = validated_data.pop("uploaded_file")
        return super().create(validated_data)

    class Meta:
        model = FileVersion
        fields = "__all__"


class FilesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    uploaded_file = serializers.FileField(write_only=True)
    versions = FileVersionSerializer(many=True, read_only=True)
    file_name = serializers.HiddenField(default=None)
    current_version = serializers.ReadOnlyField()

    class Meta:
        model = Files
        fields = [
            "file_name",
            "added_at",
            "updated_at",
            "id",
            "user",
            "versions",
            "uploaded_file",
            "current_version",
            "file_name",
        ]
