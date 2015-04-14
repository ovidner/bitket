# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES

import re

from localflavor.se.forms import SWEDISH_ID_NUMBER
from localflavor.se.utils import validate_id_birthday, id_number_checksum


# People with short names may have shorter LiU IDs!
LIU_ID = re.compile(r'^(?P<name>[a-z]{4,5})(?P<code>\d{2,3})$')


class PublicNameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.public_name


class LiUIDField(forms.CharField):
    """
    A form field that validates input as a LiU id.
    """

    def __init__(self, employee_id=True, student_id=True, *args, **kwargs):
        self.employee_id = employee_id
        self.student_id = student_id
        super(LiUIDField, self).__init__(*args, **kwargs)

    default_error_messages = {
        'invalid': _('Enter a valid LiU ID.'),
        'employee_id': _('Employee LiU IDs are not allowed.'),
        'student_id': _('Student LiU IDs are not allowed.'),
        }

    def clean(self, value):
        value = super(LiUIDField, self).clean(value)

        if value in EMPTY_VALUES:
            return None

        match = LIU_ID.match(value)
        if match is None:
            raise forms.ValidationError(self.error_messages['invalid'])

        gd = match.groupdict()

        if not self.employee_id and len(gd['code']) == 2:
            raise forms.ValidationError(self.error_messages['employee_id'])

        if not self.student_id and len(gd['code']) == 3:
            raise forms.ValidationError(self.error_messages['student_id'])

        return value


class SEPersonalIdentityNumberField(forms.CharField):
    """
    A form field that validates input as a Swedish personal identity number
    (personnummer).

    The correct formats are YYYYMMDD-XXXX, YYYYMMDDXXXX, YYMMDD-XXXX,
    YYMMDDXXXX and YYMMDD+XXXX. XXXX can be 0000.

    A + indicates that the person is older than 100 years, which will be taken
    into consideration when the date is validated.

    The birth date is checked to be a valid date.

    By default, co-ordination numbers (samordningsnummer) will be accepted. To
    only allow real personal identity numbers, pass the keyword argument
    coordination_number=False to the constructor.

    Returns (date, code) where date is a datetime.date object and code is a string with the last four characters or None
    if input was YYMMDD-0000.
    """

    def __init__(self, coordination_number=True, *args, **kwargs):
        self.coordination_number = coordination_number
        super(SEPersonalIdentityNumberField, self).__init__(*args, **kwargs)

    default_error_messages = {
        'invalid': _('Enter a valid Swedish personal identity number or YYMMDD-0000.'),
        'coordination_number': _('Co-ordination numbers are not allowed.'),
        }

    def clean(self, value):
        value = super(SEPersonalIdentityNumberField, self).clean(value)

        if value in EMPTY_VALUES:
            return None, None

        match = SWEDISH_ID_NUMBER.match(value)
        if match is None:
            raise forms.ValidationError(self.error_messages['invalid'])

        gd = match.groupdict()

        code = str(gd['serial'] + gd['checksum'])

        # compare the calculated value with the checksum
        # if id_number_checksum(gd) != int(gd['checksum']):
        # raise forms.ValidationError(self.error_messages['invalid'])

        # check for valid birthday
        try:
            birth_day = validate_id_birthday(gd)
        except ValueError:
            raise forms.ValidationError(self.error_messages['invalid'])

        # make sure that co-ordination numbers do not pass if not allowed
        if not self.coordination_number and int(gd['day']) > 60:
            raise forms.ValidationError(self.error_messages['coordination_number'])

        if code == '0000':
            return birth_day, None

        return birth_day, code
