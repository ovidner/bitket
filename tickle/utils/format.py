# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal


def format_decimal(d):
    """
    Removes exponent and trailing zeros from Decimal numbers.
    """
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def format_percent(d):
    """
    Returns a pretty formatted percent from a decimal factor, e.g. 0.25 ==> 25 %
    """

    return '{0} %'.format(format_decimal(d * Decimal(100)))
