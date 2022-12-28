from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES_ROLE = (
    ("user", "user"),
    ("admin", "admin"),
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer.',
                   'Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': "Пользователь с таким username уже существует.",
        },
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "Пользователь с таким email уже существует.",
        },
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )
    role = models.CharField(
        max_length=10,
        default="user",
        choices=CHOICES_ROLE,
    )
    dev_password = models.TextField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
