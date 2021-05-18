import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import model_to_dict
from .managers import UserManager
from stdimage import JPEGField
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=255, verbose_name='Nombre',null=True, )
    last_name = models.CharField(max_length=255, verbose_name='Apellido',null=True, )
    email = models.EmailField(unique=True, verbose_name="Correo Electronico")
    direction = models.CharField(max_length=70, verbose_name='Direccion', null=True, )
    province = models.CharField(max_length=70, verbose_name='Provincia', null=True, )
    country = models.CharField(max_length=70, verbose_name='Pais', null=True, )
    telephone = models.CharField(max_length=70, verbose_name='Telefono', null=True, )
    avatar = JPEGField(
        upload_to='users/avatar/',
        variations={
            'thumbnail': {"width": 100, "height": 100, "crop": True}
        },
        null=True, blank=True)

    is_active = models.BooleanField(default=True)  # Indica si el usuario esta activo
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'  # Identificador unico
    REQUIRED_FIELDS = []  # Lista de nombres que solicita al crear un superusuario

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-id']

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return os.path.join(settings.MEDIA_URL + str('users/avatar/male.png'))


