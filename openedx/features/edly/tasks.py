from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from celery.task import task
from celery.utils.log import get_task_logger
from edx_ace import ace
from edx_ace.recipient import Recipient
from lms.djangoapps.instructor.enrollment import send_mail_to_student
from openedx.core.lib.celery.task_utils import emulate_http_request
from openedx.features.edly.message_types import HandoutChangeNotification, OutlineChangeNotification

TASK_LOG = get_task_logger(__name__)
ROUTING_KEY = getattr(settings, 'ACE_ROUTING_KEY')


@task(routing_key=ROUTING_KEY)
def send_bulk_mail_to_students(students, param_dict, message_type):
    """
    This task is responsible for sending the email to all of the students using the ChangesEmail Message type.

    Arguments
        students: List of enrolled students to whom we want to send email.
        param_dict: Parameters to pass to the email template.
        message_type: String contains the type of changes.
    """
    message_types = {
        'outline_changes': OutlineChangeNotification,
        'handout_changes': HandoutChangeNotification
    }
    message_class = message_types[message_type]
    param_dict['site'] = Site.objects.get(id=param_dict['site_id'])
    for student_id in students:
        student = User.objects.get(id=student_id)
        param_dict['full_name'] = student.profile.name
        message = message_class().personalize(
            recipient=Recipient(username='', email_address=student.email),
            language='en',
            user_context=param_dict,
        )
        with emulate_http_request(site=param_dict['site'], user=student):
            TASK_LOG.info(
                u'Attempting to send %s changes email to: %s, for course: %s',
                message_type,
                student.email,
                param_dict['course_name']
            )
            try:
                ace.send(message)
                TASK_LOG.info(
                    u'Success: Task sending email for %s change to: %s , For course: %s',
                    message_type,
                    student.email,
                    param_dict['course_name']
                )
            except Exception:  # pylint: disable=broad-except
                TASK_LOG.exception(
                    u'Failure: Task sending email for %s change to: %s , For course: %s',
                    message_type,
                    student.email,
                    param_dict['course_name']
                )


@task(routing_key=ROUTING_KEY)
def send_course_enrollment_mail(user_email, email_params):
    TASK_LOG.info(
        u'Attempting to send course enrollment email to: %s, for course: %s',
        user_email,
        email_params['display_name']
    )
    try:
        send_mail_to_student(user_email, email_params)
        TASK_LOG.info(
            u'Success: Task sending email to: %s , For course: %s',
            user_email,
            email_params['display_name']
        )
    except Exception:  # pylint: disable=broad-except
        TASK_LOG.exception(
            u'Failure: Task sending email tos: %s , For course: %s',
            user_email,
            email_params['display_name']
        )
