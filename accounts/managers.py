from django.db import models
from django.db.models.query import QuerySet


class BusinessManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(user_role__name='Business')


class ClientManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(user_role__name='Client')
