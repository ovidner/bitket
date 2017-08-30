from django import forms
from django.conf import settings
from django.core import signing
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class StripeScopeField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            ('read_only', _('Read Only')),
            ('read_write', _('Read/Write'))
        )
        kwargs['default'] = 'read_write'
        super(StripeScopeField, self).__init__(*args, **kwargs)


class StripeStateField(forms.CharField):
    def to_python(self, value):
        try:
            organizer, session = signing.loads(
                value, max_age=settings.STRIPE_OAUTH_TIMEOUT)
        except signing.SignatureExpired:
            raise ValidationError(
                _('Request signature has expired. Please try again.'),
                code='signature_expired')
        except signing.BadSignature:
            raise ValidationError(_('Invalid request signature.'),
                                  code='signature_invalid')

        return {'organizer': organizer, 'session': session}


class StripeConnectCallbackForm(forms.Form):
    code = forms.CharField()
    scope = StripeScopeField()
    state = StripeStateField()
