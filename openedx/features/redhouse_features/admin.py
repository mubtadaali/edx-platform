"""
Register redhouse multi-site admin panels
"""
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.db.models import Q

from django.contrib.auth.models import Permission

from django.contrib.auth import get_user_model

from openedx.features.edly.models import EdlyUserProfile, EdlySubOrganization


User = get_user_model()


class RedhouseAdminSite(AdminSite):
    site_header = "Redhouse site 1"
    site_title = "Redhouse site 1"
    index_title = "Welcome to Redhouse site 1"

redhouse_1_admin_site = RedhouseAdminSite(name='redhouse_1_admin')

# Assign the permissions according to the requirements
# e,g, assign user permission to a staff user (non super user) to enable them to
# view users table on `redhouse-admin` site


class SiteQuerysetMixin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(SiteQuerysetMixin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs

        request_site = request.site
        queries = Q()

        for site_filter in self.site_filters:
            queries |= Q(**{
                site_filter: request_site
            })

        return qs.filter(queries)


class UserAdmin(SiteQuerysetMixin):
    site_filters = (
        'edly_profile__edly_sub_organizations__lms_site',
        'edly_profile__edly_sub_organizations__studio_site'
    )


class EdlyUserProfileAdmin(SiteQuerysetMixin):
    site_filters = (
        'edly_sub_organizations__lms_site',
        'edly_sub_organizations__studio_site'
    )


class EdlySubOrganizationAdmin(SiteQuerysetMixin):
    site_filters = (
        'lms_site',
        'studio_site'
    )


redhouse_1_admin_site.register(EdlyUserProfile, EdlyUserProfileAdmin)
redhouse_1_admin_site.register(User, UserAdmin)
redhouse_1_admin_site.register(EdlySubOrganization, EdlySubOrganizationAdmin)
