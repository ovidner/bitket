import re

from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

from localflavor.se.utils import validate_id_birthday


# People with short names may have shorter LiU IDs!
LIU_ID = re.compile(r'^(?P<name>[a-z]{4,5})(?P<code>\d{2,3})$')


# Originally from localflavor.se.forms but patched for interimspersonnummer
# where the 7th (or 9th) position may be A-Z. This letter counts as a 1 when
# calculating Luhn checksum. See more at
# https://portal.nordu.net/display/Inkubator/norEduPersonNIN+och+Svenska+Personnummer and
# https://confluence.its.umu.se/confluence/display/Publik/Interrimspersonnummer
SWEDISH_ID_NUMBER = re.compile(r'^(?P<century>\d{2})?(?P<year>\d{2})'
                               r'(?P<month>\d{2})(?P<day>\d{2})(?P<sign>[\-+])'
                               r'?(?P<serial>\d{3}|[A-Za-z]\d{2})'
                               r'(?P<checksum>\d)$')


# Originally from localflavor.se.forms but patched for interimspersonnummer.
# See above.
def id_number_checksum(gd):
    """
    Calculates a Swedish ID number checksum, using the Luhn algorithm
    """
    n = s = 0
    for c in (gd['year'] + gd['month'] + gd['day'] + gd['serial']):
        # Letter? It's an interimspersonnummer and we substitute the letter
        # with 1.
        if c.isalpha():
            c = 1

        tmp = ((n % 2) and 1 or 2) * int(c)

        if tmp > 9:
            tmp = sum([int(i) for i in str(tmp)])

        s += tmp
        n += 1

    if (s % 10) == 0:
        return 0

    return (((s // 10) + 1) * 10) - s


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

    Returns (date, code) where date is a datetime.date object and code is a
    string with the last four characters or None if input was YYMMDD-0000.
    """

    def __init__(self, coordination_number=True, interim_number=True, *args, **kwargs):
        self.coordination_number = coordination_number
        self.interim_number = interim_number
        super(SEPersonalIdentityNumberField, self).__init__(*args, **kwargs)

    default_error_messages = {
        'invalid': _('Enter a valid Swedish personal identity number or YYMMDD-0000.'),
        'coordination_number': _('Co-ordination numbers are not allowed.'),
        'interim_number': _('Interim numbers are not allowed.'),
        }

    def clean(self, value):
        value = super(SEPersonalIdentityNumberField, self).clean(value)

        if value in EMPTY_VALUES:
            return None, None, False

        match = SWEDISH_ID_NUMBER.match(value)
        if match is None:
            raise forms.ValidationError(self.error_messages['invalid'])

        gd = match.groupdict()

        code = str(gd['serial'] + gd['checksum'])
        is_coordination_number = int(gd['day']) > 60

        # make sure that co-ordination numbers do not pass if not allowed
        if not self.coordination_number and is_coordination_number:
            raise forms.ValidationError(self.error_messages['coordination_number'])

        # make sure that interim numbers do not pass if not allowed
        if not self.interim_number and gd['serial'][0].isalpha():
            raise forms.ValidationError(self.error_messages['interim_number'])

        # compare the calculated value with the checksum, only if other than 0000
        if code != '0000' and id_number_checksum(gd) != int(gd['checksum']):
            raise forms.ValidationError(self.error_messages['invalid'])

        # check for valid birthday
        try:
            birth_day = validate_id_birthday(gd)
        except ValueError:
            raise forms.ValidationError(self.error_messages['invalid'])

        if code == '0000':
            return birth_day, None, False

        return birth_day, code, is_coordination_number


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
