from django.db import models
from apps.base.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
# from simple_history.models import HistoricalRecords

class Rol(BaseModel):
    rol = models.CharField('Rol del usuario', max_length = 50, null = False, blank = False, unique = True)

    class Meta:
        ordering = ['rol',]
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.rol

    def save(self, *args, **kwargs):
        permisos_defecto = ['add', 'change', 'delete', 'view']
        if not self.id:
            nuevo_grupo, creado = Group.objects.get_or_create(name = f'{self.rol}')
            for permiso in permisos_defecto:
                permiso, creado = Permission.objects.update_or_create(
                    name = f'can {permiso} {self.rol}',
                    content_type = ContentType.objects.get_for_model(Rol),
                    codename = f'{permiso}_{self.rol}'
                )
                if creado:
                    nuevo_grupo.permissions.add(permiso.id)
            super().save(*args, **kwargs)

        else:
            rol_antiguo = Rol.objects.filter(id == self.id).values('rol').firts()
            if rol_antiguo['rol'] == self.rol:
                super().save(*args, **kwargs)
            else:
                Group.objects.filter(name = rol_antiguo['rol']).update(name = f'{self.rol}')
                for permiso in permisos_defecto:
                    Permission.objects.filter(codename = f"{permiso}_{rol_antiguo['rol']}").update(
                        codename = f'{permiso}_{self.rol}',
                        name = f'can {permiso} {self.rol}'
                    )
                super().save(*args, **kwargs)

class UserManager(BaseUserManager):
    def _create_user(self,username,email,password,is_staff,is_superuser,**extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password = None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password = None, **extra_fields):
        return self._create_user(username,email, password, True, True, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Usuario', max_length=100, unique = True)
    email = models.EmailField('Email', max_length=150, unique = True)
    imagen = models.ImageField('Imagen de perfil', upload_to=None, max_length=200, null = True, blank = True)
    rol = models.ForeignKey(Rol, on_delete = models.CASCADE, null = True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    # historical = HistoricalRecords()
    objects = UserManager()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['username']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            if self.rol is not None:
                grupo = Group.objects.filter(name = self.rol.rol).first()
                if grupo:
                    self.groups.add(grupo)
                super.save(*args, **kwargs)
            else:
                if self.rol is not None:
                    grupo_atiguo = Usuario.objects.filter(id = self.id).values('rol__rol').first()
                    if grupo_atiguo['rol__rol'] == self.rol.rol:
                        super().save(*args, **kwargs)
                    else:
                        grupo_anterior = Group.objects.filter(name = grupo_atiguo['rol__rol']).first()
                        if grupo_anterior:
                            self.groups.remove(grupo_anterior)
                        nuevo_grupo = Group.objects.filter(name = self.rol.rol).first()
                        if nuevo_grupo:
                            self.groups.add(nuevo_grupo)
                        super().save(*args, **kwargs)