from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField


class IdField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('primary_key', True)
        kwargs['default'] = kwargs.get('default', uuid4)
        kwargs['editable'] = False
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('ID'))
        super(IdField, self).__init__(*args, **kwargs)


class StripValueMixin(object):
    strip_chars = None

    def clean(self, value, model_instance):
        value = value.strip(self.strip_chars)
        return super(StripValueMixin, self).clean(value, model_instance)


class DescriptionField(models.TextField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('description'))
        super(DescriptionField, self).__init__(*args, **kwargs)


class MoneyField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = kwargs.get('max_digits', 12)
        kwargs['decimal_places'] = 2
        super(MoneyField, self).__init__(*args, **kwargs)


class NameField(StripValueMixin, models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('name'))
        super(NameField, self).__init__(*args, **kwargs)


class NullCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['default'] = None
        super(NullCharField, self).__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super(NullCharField, self).clean(value, model_instance)
        return value or None


class SlugField(AutoSlugField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('slug'))
        super(SlugField, self).__init__(*args, **kwargs)


class LiuIdField(StripValueMixin, NullCharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        kwargs['unique'] = True
        kwargs['verbose_name'] = _('LiU ID')
        super(LiuIdField, self).__init__(*args, **kwargs)


class PasswordField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 128
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('password'))
        super(PasswordField, self).__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super(PasswordField, self).clean(value, model_instance)
        return value or make_password(None)
