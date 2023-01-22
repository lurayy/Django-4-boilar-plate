import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


def image_directory_path(instance, *args, **kwargs):
    return f'user/{instance.username}/profile.jpg'


class UserBase(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    profile_image = models.ImageField(upload_to=image_directory_path,
                                      null=True,
                                      blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'],
                                    name='UserBase Email Unique Constraints')
        ]


class Country(models.Model):
    alpha2 = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    num = models.PositiveIntegerField()
    phone_code = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    continent = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class AuthenticationLog(models.Model):
    LOGIN_STATUS = (('login', 'Login'), ('logout', 'Logout'))
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=6,
                              choices=LOGIN_STATUS,
                              null=True,
                              blank=True)

    def __str__(self):
        return f'{self.user} {self.action} {self.datetime}'


class PasswordResetCode(models.Model):
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    email = models.EmailField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'email'],
                name='PasswordResetCode Unique Constraints')
        ]


class Settings(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
