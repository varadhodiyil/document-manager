from django.core.management.base import BaseCommand

from propylon_document_manager.file_versions.models import Files, FileVersion
from propylon_document_manager.users.models import User

file_versions = [
    "bill_document",
    "amendment_document",
    "act_document",
    "statute_document",
]


class Command(BaseCommand):
    help = "Load basic file version fixtures"

    def handle(self, *args, **options):
        users = User.objects.all()[:10]

        for user in users:
            for file_name in file_versions:
                file = Files.objects.create(file_name=file_name, user=user)
                FileVersion.objects.create(file=file, version_number=1)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(file_versions)} file versions"))
