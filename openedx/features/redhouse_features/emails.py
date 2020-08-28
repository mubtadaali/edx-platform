from openedx.core.djangoapps.ace_common.message import BaseMessageType


class SupportEmail(BaseMessageType):
    """
    Email sent to support when there is a "Contact us" form submission.
    """
