from django.db import models
from django.contrib.auth.models from BaseUseManager, AbstracBaseUser, PermissionMixin

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self.db)
        return user

    def create_user(self, username, email, password = None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password = None, **extra_fields):
        return self._create_user(username,email, password, True, True, **extra_fields)

class User(AbstracBaseUser, PermissionMixin):
    username = models.CharField(_("Usuario"), max_length=100, unique = True)
    email = models.EmailField(_("Email"), max_length=150, unique = True)
    image = models.ImageField(_("Imagen de perfil"), upload_to=None, max_length=200, null = True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'

