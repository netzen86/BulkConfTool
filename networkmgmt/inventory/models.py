from django.db import models
from django.contrib.auth import get_user_model
from core.keys_to_tup import keys_to_tup


User = get_user_model()


CHOICES_DEV_TYPE = (
    ('router', 'router'),
    ('switch', 'switch'),
)

CHOICES_SSH_TYPE = keys_to_tup()


class Devices(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    # This field is used by netmiko to connect to the device.
    device_type = models.CharField(
        max_length=21,
        default=None,
        choices=CHOICES_SSH_TYPE,
    )
    ip_add = models.GenericIPAddressField()
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='devices',
    )
    type = models.CharField(
        max_length=10,
        default=None,
        choices=CHOICES_DEV_TYPE,
    )
    serial_num = models.TextField()
    model = models.TextField()
    hostname = models.TextField()
    os_version = models.TextField()
    vendor = models.TextField()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    def __str__(self):
        return self.hostname


class Configurations(models.Model):
    device = models.ForeignKey(
        Devices,
        on_delete=models.CASCADE,
        related_name='devices',
        verbose_name='Устройство'
    )
    configuration = models.TextField()

    class Meta:
        ordering = ('device',)
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурации'

    def __str__(self):
        return self.device
