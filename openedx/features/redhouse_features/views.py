import json
from logging import getLogger

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from rest_framework import status

from openedx.features.redhouse_features.utils import send_notification_email_to_support


logger = getLogger(__name__)


@require_http_methods(["POST"])
def email_support(request):
    body = json.loads(request.body)

    try:
        send_notification_email_to_support(
            subject=body['subject'],
            body=body['comment']['body'],
            name=body['requester']['name'],
            email=body['requester']['email'],
            course=body['custom_fields'][0]['value']
        )

        return HttpResponse(status=status.HTTP_201_CREATED)

    except Exception:
        logger.error('Error occurred while trying to send contact-support email.', exc_info=True)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
