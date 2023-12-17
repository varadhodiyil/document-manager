from django.contrib.auth import get_user_model
from django.db import models
from propylon_document_manager.file_versions.api.utils import get_upload_path


class Files(models.Model):
    id = models.AutoField(primary_key=True)
    file_url = models.fields.CharField(max_length=512)
    file_name = models.fields.CharField(max_length=512)
    user = models.ForeignKey(get_user_model(), related_name="file_user", on_delete=models.PROTECT)
    added_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    current_version = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("file_url", "user")


class FileVersion(models.Model):
    file = models.ForeignKey(Files, on_delete=models.CASCADE, related_name="versions")
    version_number = models.fields.IntegerField()
    added_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField(upload_to=get_upload_path, max_length=500)
    file_hash = models.CharField(max_length=40)

    class Meta:
        unique_together = ("file", "version_number")
