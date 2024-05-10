from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import BusinessManager, ClientManager


# Create your models here.
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Roles(TimeStampedModel):
    name = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        db_table = 'roles'

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True)
    user_role = models.ForeignKey(
        Roles, on_delete=models.CASCADE, null=True, blank=True
    )


class Business(User):
    objects = BusinessManager()

    def save(self, *args, **kwargs):
        if not self.user_role:
            self.user_role, created = Roles.objects.get_or_create(
                name='Business', description='Business User Account'
            )
        super().save(*args, **kwargs)

    class Meta:
        proxy = True


class Client(User):
    objects = ClientManager()

    def save(self, *args, **kwargs):
        if not self.user_role:
            self.user_role, created = Roles.objects.get_or_create(
                name='Client', description='Client User Account'
            )
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
