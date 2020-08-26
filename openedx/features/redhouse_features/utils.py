import logging

from django.conf import settings

from edx_ace import ace
from edx_ace.recipient import Recipient
from openedx.core.djangoapps.ace_common.template_context import get_base_template_context
from openedx.core.djangoapps.theming.helpers import get_current_site

from openedx.features.redhouse_features.emails import SupportEmail


log = logging.getLogger(__name__)

EMAIL_CLASSES = {
    'support': SupportEmail
}


def send_notification_email_to_support(subject, body, name, email, additional_info=None, course=None):
    """
    Sending a notification-email to the Support Team.

    Arguments:
        subject         - Email subject
        body            - Email body
        name            - username of the requester user
        email           - email of the requester user
        additional_info - Any additional fields for email body
        course          - Name of the course (filled from the form)
    """
    key = 'support'
    dest_emails = settings.SUPPORT_DESK_EMAILS
    data = {
        'name': name,
        'email': email,
        'body': body,
        'course': course,
        'additional_info': additional_info,
    }
    send_notification(key, data, subject, dest_emails)


def send_notification(key, data, subject=None, dest_emails=[]):
    """
    Send an email notification to provided email addresses.

    Arguments:
        key         - Email template will be selected on the basis of key
        data        - Dict containing context/data for the template
        subject     - Email subject
        dest_emails - List of destination emails

    """
    site = get_current_site()
    message_context = get_base_template_context(site)

    message_context.update(data)

    if subject:
        message_context['subject'] = subject

    for email in dest_emails:
        log.info('Sending support email with subject "{}" to {}'.format(
            subject, email
        ))

        msg = EMAIL_CLASSES[key]().personalize(
            recipient=Recipient(username='', email_address=email),
            language=settings.LANGUAGE_CODE,
            user_context=message_context,
        )
        ace.send(msg)
