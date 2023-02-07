from django.urls import path
from .views import (
    switch_port_mgmt,
    MainView,
    SwitchPortSearchFormView,
    SwitchPortMgmtFormView
)

app_name = 'swportmgmt'


urlpatterns = [
    # path('', switch_port_mgmt, name='switch_port_mgmt'),
    path('', MainView.as_view(), name='switch_port_mgmt'),
    path('search/', SwitchPortSearchFormView.as_view(), name='search'),
    path('switchportmgmt/', SwitchPortMgmtFormView.as_view(), name='switchportmgmt'),
]
