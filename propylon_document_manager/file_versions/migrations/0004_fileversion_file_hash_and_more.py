# Generated by Django 4.1.9 on 2023-12-16 00:46

from django.db import migrations, models
import propylon_document_manager.file_versions.api.utils


class Migration(migrations.Migration):
    dependencies = [
        ("file_versions", "0003_files_file_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileversion",
            name="file_hash",
            field=models.CharField(default="", max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="fileversion",
            name="uploaded_file",
            field=models.FileField(
                max_length=500, upload_to=propylon_document_manager.file_versions.api.utils.get_upload_path
            ),
        ),
    ]
