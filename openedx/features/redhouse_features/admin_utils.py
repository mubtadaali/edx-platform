
from six import iteritems
from django.conf.urls import include, url

from .admin import redhouse_1_admin_site

SITES = {
    'redhouse': redhouse_1_admin_site
}


def add_admin_sites(urlpatters):
    for site, admin in iteritems(SITES):
        urlpatters += url(r'{}-admin'.format(site), include(admin.urls)),
