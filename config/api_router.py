from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from propylon_document_manager.users.api.views import UserViewSet, RegisterViewSet
from propylon_document_manager.file_versions.api.views import FileVersionViewSet, FilesViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("register", RegisterViewSet)
router.register("users", UserViewSet)
router.register("file_versions", FileVersionViewSet)
router.register("files", FilesViewSet)


app_name = "api"
urlpatterns = router.urls
