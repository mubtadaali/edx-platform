"""
URLs for the redhouse admin panel.
"""
from django.conf.urls import url, include

from openedx.features.redhouse_features.admin_panel.views import AdminPanelView


app_name = 'redhouse_admin_panel'

urlpatterns = [
    url(r'', AdminPanelView.as_view(), name='admin_dashboard'),
    url(r'api/v0/', include('openedx.features.redhouse_features.admin_panel.api.v0.urls'))
]
