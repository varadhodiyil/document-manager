from django.contrib.auth import get_user_model
from django.db import models


class Files(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.fields.CharField(max_length=512)
    user = models.ForeignKey(get_user_model(), related_name="file_user", on_delete=models.PROTECT)
    added_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    current_version = models.PositiveIntegerField(default=1)


class FileVersion(models.Model):
    file = models.ForeignKey(Files, on_delete=models.CASCADE, related_name="versions")
    version_number = models.fields.IntegerField()
    added_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("file", "version_number")
