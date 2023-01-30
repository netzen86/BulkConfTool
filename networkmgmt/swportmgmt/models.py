from django.db import models
from django.contrib.auth import get_user_model
from inventory.views import Devices
User = get_user_model()


class SwitchPort(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    switch = models.ForeignKey(
        Devices,
        on_delete=models.CASCADE,
        related_name='switches',
        verbose_name='Устройство'
    )
    port = models.CharField(max_length=254)
    socket = models.CharField(max_length=254)
    description = models.CharField(max_length=254)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Порты коммутатора'
        verbose_name_plural = 'Порты коммутаторов'

    def __str__(self):
        return self.switch.ip_add


class Vlans(models.Model):
    switch = models.ForeignKey(
        Devices,
        on_delete=models.CASCADE,
        related_name='vlans',
        verbose_name='Switch',
        limit_choices_to={'type': 'switch'},
    )
    vid = models.IntegerField()
    vlan_name = models.CharField(
        max_length=254
    )
    group = None

    class Meta:
        ordering = ('vid',)
        verbose_name = 'VLAN'
        verbose_name_plural = 'VLANs'

    def __str__(self):
        return f'{self.vid} {self.vlan_name}'


class SwitchPortMgmt(models.Model):
    switch = models.ForeignKey(
        SwitchPort,
        on_delete=models.CASCADE,
        related_name='portmgmt',
        verbose_name='Коммутатор'
    )
    port = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    mac = models.CharField(
        max_length=254
    )
    change_vlan = models.ForeignKey(
        Vlans,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Ch VLAN',
    )

    # models.CharField(
    #     max_length=10,
    #     choices=Vlans.objects.filter(switch_id=F('switch_id'))
    # )
    
    shut_port = models.BooleanField(default=False)
    clear_mac = models.BooleanField(default=False)
    state = models.CharField(
        max_length=254
    )
    on_off = models.CharField(
        max_length=254
    )
    connect = models.CharField(
        max_length=254
    )
