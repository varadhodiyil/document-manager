from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from propylon_document_manager.file_versions.api.utils import generate_hash
from propylon_document_manager.file_versions.models import Files, FileVersion
from propylon_document_manager.users.models import User

file_versions = [
    "bill_document",
    "amendment_document",
    "act_document",
    "statute_document",
]


def make_file(name: str) -> ContentFile:
    return ContentFile(name)


class Command(BaseCommand):
    help = "Load basic file version fixtures"

    def handle(self, *args, **options):
        users = User.objects.all()[:10]

        for user in users:
            for file_name in file_versions:
                try:
                    file = Files.objects.create(file_name=file_name, user=user, file_url=f"/document/url_{file_name}")
                    content_file = make_file(file_name)
                    FileVersion.objects.create(
                        file=file, version_number=1, uploaded_file=content_file, file_hash=generate_hash(content_file)
                    )
                except IntegrityError:
                    print("File Exists Skipping")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(file_versions)} file versions"))
