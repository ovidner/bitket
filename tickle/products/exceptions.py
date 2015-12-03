from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ValidationError


class ConflictingProductVariationChoices(ValidationError):
    pass


class ExceedsLimit(ValidationError):
    pass


class ModifiesHistory(ValidationError):
    pass
