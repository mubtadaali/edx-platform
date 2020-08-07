"""
Sync users data according to multisites requirements
"""
import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from course_creators.models import CourseCreator
from student.roles import CourseInstructorRole
from student.models import CourseAccessRole

from openedx.features.edly.models import EdlyUserProfile, EdlySubOrganization


log = logging.getLogger(__name__)
User = get_user_model()

DEFAULT_SUB_ORGANIZATION = 'redhouse'
DEFAULT_ORGANIZATION = 'redhouse'


class Command(BaseCommand):
    """
    Sync users data according to multisites requirements

    This command MUST be run in cms.

    Format:
        python manage.py cms sync_users_data [sub_organization [organization]]
    """

    def add_arguments(self, parser):
        parser.add_argument('sub_organization', nargs='?', default=DEFAULT_SUB_ORGANIZATION, type=str)
        parser.add_argument('organization', nargs='?', default=DEFAULT_ORGANIZATION, type=str)

    def handle(self, *args, **options):
        sub_organization = options['sub_organization']
        organization = options['organization']

        users = User.objects.filter(is_superuser=False)
        staff_users = users.filter(is_staff=True)

        sub_org = self.get_sub_organization(sub_organization)

        linked_users_count = 0
        course_creator_count = 0
        course_access_roles_count = 0

        for user in users:
            if self.create_and_link_edly_profiles(user, sub_org):
                linked_users_count += 1

        for user in staff_users:
            if self.create_course_creator(user):
                course_creator_count += 1

            if  self.create_course_access_roles(user, organization):
                course_access_roles_count += 1

        map(self.remove_staff_access, staff_users)

        log.info('Edly user profiles are successfully created for %d user(s)', linked_users_count)
        log.info('Course creator objects are successfully created for %d user(s)', course_creator_count)
        log.info('Course access roles are successfully created for %d user(s)', course_access_roles_count)
        log.info('Staff access is removed for %d user(s)', len(staff_users))

    def get_sub_organization(self, sub_org_slug):
        try:
            return EdlySubOrganization.objects.get(slug=sub_org_slug)
        except EdlySubOrganization.DoesNotExist:
            log.error('Edly sub organization %s does not exist', sub_org_slug)
            exit(1)

    def create_and_link_edly_profiles(self, user, sub_org):
        try:
            edly_profile = EdlyUserProfile.objects.get(user=user)
            log.info(
                'Found existing edly user profile %s linked with sub org %s',
                user.username,
                sub_org
            )
            return
        except EdlyUserProfile.DoesNotExist:
            edly_profile = EdlyUserProfile.objects.create(user=user)
            edly_profile.edly_sub_organizations.add(sub_org)
            edly_profile.save()
            log.info(
                'Created edly user profile for user %s and linked with sub org %s',
                user.username,
                sub_org
            )
            return edly_profile

    def create_course_creator(self, user):
        try:
            course_creator = CourseCreator.objects.get(user=user)
            log.info(
                'Found existing CourseCreator for user %s with state %s',
                user.username,
                course_creator.state
            )
            return
        except CourseCreator.DoesNotExist:
            course_creator = CourseCreator.objects.create(
                user=user,
                state=CourseCreator.GRANTED,
                note='Auto-generated using the management command.'
            )

            log.info(
                'Created CourseCreator for user %s with status %s',
                user.username,
                CourseCreator.GRANTED
            )

            return course_creator

    def create_course_access_roles(self, user, org):
        try:
            course_access_role = CourseAccessRole.objects.get(user=user)
            log.info(
                'Found existing access role for user %s with role %s',
                user.username,
                course_access_role.role
            )
        except CourseAccessRole.DoesNotExist:
            course_access_role = CourseAccessRole.objects.create(
                user=user,
                org=org,
                role=CourseInstructorRole.ROLE
            )
            log.info(
                'Created CourseAccessRole with Instructor role for user %s.',
                user.username
            )
            return course_access_role

    def remove_staff_access(self, user):
        user.is_staff = False
        user.save()
        log.info('Removed staff access for user %s', user.username)
