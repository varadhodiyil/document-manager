from typing import Any
from rest_framework import serializers
from propylon_document_manager.file_versions.api.utils import generate_hash

from propylon_document_manager.file_versions.models import Files, FileVersion


class FileVersionSerializer(serializers.ModelSerializer):
    version_number = serializers.ReadOnlyField(read_only=True)
    file_hash = serializers.HiddenField(write_only=True, default=None)

    def validate(self, attrs: Any) -> bool:
        current_hash = generate_hash(attrs["uploaded_file"])
        has_similiar_version = FileVersion.objects.filter(file=attrs["file"], file_hash=current_hash).count()
        if has_similiar_version:
            raise serializers.ValidationError("File Version already exits")
        attrs["file_hash"] = current_hash
        return attrs

    class Meta:
        model = FileVersion
        fields = "__all__"


class FilesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    uploaded_file = serializers.FileField(write_only=True)
    versions = FileVersionSerializer(many=True, read_only=True)
    current_version = serializers.ReadOnlyField()
    file_name = serializers.ReadOnlyField()

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
            "file_url",
        ]
