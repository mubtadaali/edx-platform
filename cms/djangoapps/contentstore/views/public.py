"""
Public views
"""


from django.conf import settings
from django.shortcuts import redirect
from django.utils.http import urlquote_plus
from waffle.decorators import waffle_switch

from contentstore.config import waffle
from edxmako.shortcuts import render_to_response

__all__ = ['register_redirect_to_lms', 'login_redirect_to_lms', 'howitworks', 'accessibility']


def register_redirect_to_lms(request):
    """
    This view redirects to the LMS register view. It is used to temporarily keep the old
    Studio signup url alive.
    """
<<<<<<< HEAD
    # Redirect user to LMS login page if `DISABLE_STUDIO_SSO_OVER_LMS` feature
    # flag is not enabled and user tries to access the signin page using URL.
    if not settings.FEATURES.get('DISABLE_STUDIO_SSO_OVER_LMS', False):
        return redirect_with_get(settings.FRONTEND_LOGIN_URL, request.GET, False)

    csrf_token = csrf(request)['csrf_token']
    if request.user.is_authenticated:
        return redirect('/course/')
    if (settings.FEATURES['AUTH_USE_CERTIFICATES'] and
            ssl_get_cert_from_request(request)):
        # SSL login doesn't require a login view, so redirect
        # to course now that the user is authenticated via
        # the decorator.
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('/course/')
    if settings.FEATURES.get('AUTH_USE_CAS'):
        # If CAS is enabled, redirect auth handling to there
        return redirect(reverse('cas-login'))

    return render_to_response(
        'login.html',
        {
            'csrf': csrf_token,
            'forgot_password_link': "//{base}/login#forgot-password-modal".format(base=settings.LMS_BASE),
            'platform_name': configuration_helpers.get_value('platform_name', settings.PLATFORM_NAME),
        }
=======
    register_url = '{register_url}{params}'.format(
        register_url=settings.FRONTEND_REGISTER_URL,
        params=_build_next_param(request),
>>>>>>> 63ff8fe07fcec03d5d89d251a7a80f907e3e3d71
    )
    return redirect(register_url, permanent=True)


def login_redirect_to_lms(request):
    """
    This view redirects to the LMS login view. It is used for Django's LOGIN_URL
    setting, which is where unauthenticated requests to protected endpoints are redirected.
    """
    login_url = '{login_url}{params}'.format(
        login_url=settings.FRONTEND_LOGIN_URL,
        params=_build_next_param(request),
    )
    return redirect(login_url)


def _build_next_param(request):
    """ Returns the next param to be used with login or register. """
    next_url = request.GET.get('next')
    next_url = next_url if next_url else settings.LOGIN_REDIRECT_URL
    if next_url:
        # Warning: do not use `build_absolute_uri` when `next_url` is empty because `build_absolute_uri` would
        # build use the login url for the next url, which would cause a login redirect loop.
        absolute_next_url = request.build_absolute_uri(next_url)
        return '?next=' + urlquote_plus(absolute_next_url)
    return ''


def howitworks(request):
    "Proxy view"
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        return render_to_response('howitworks.html', {})


@waffle_switch('{}.{}'.format(waffle.WAFFLE_NAMESPACE, waffle.ENABLE_ACCESSIBILITY_POLICY_PAGE))
def accessibility(request):
    """
    Display the accessibility accommodation form.
    """

    return render_to_response('accessibility.html', {
        'language_code': request.LANGUAGE_CODE
    })
