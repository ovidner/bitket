from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class DefaultException(APIException):
    pass


class ClientErrorMixin(object):
    status_code = status.HTTP_400_BAD_REQUEST


class PaymentDenied(DefaultException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('The payment was denied.')


class EventProductLimitExceeded(DefaultException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Exceeding event quantity limit.')


class PersonalProductLimitExceeded(DefaultException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Exceeding personal quantity limit.')


class TotalProductLimitExceeded(DefaultException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Exceeding total quantity limit.')


class ModifiesHistory(DefaultException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Modifies history.')
