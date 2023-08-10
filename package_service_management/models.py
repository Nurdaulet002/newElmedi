from django.db import models
from .abstract_models import PackageMixin, PackageServiceMixin


# Пакеты
class Package(PackageMixin):
    pass


# Услуги пакета
class PackageService(PackageServiceMixin):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
