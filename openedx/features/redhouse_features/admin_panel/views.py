"""
Sites admin dashboard views.
"""
from logging import getLogger
from django.conf import settings
from django.views.generic import View
from edxmako.shortcuts import render_to_response

from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


logger = getLogger(__name__)


class AdminPanelView(View):
    """
    View for admin panel dashboard.
    """

    def get(self, request):
        context = {
            'platform_name': configuration_helpers.get_value('platform_name', settings.PLATFORM_NAME),
        }

        return render_to_response('admin_panel/dashboard.html', context)
