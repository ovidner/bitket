# -*- coding: utf-8 -*-
from baluhn import generate as baluhn_generate, verify as baluhn_verify
from django.conf import settings


def generate(reference, check_length=settings.INVAR_OCR_CHECK_LENGTH):
    reference = str(reference)
    assert check_length == 1 or check_length == 2

    if check_length == 1:
        return reference + baluhn_generate(reference)
    elif check_length == 2:
        long_reference = reference + str(len(reference) + 2)
        return long_reference + baluhn_generate(long_reference)


def strip(ocr, check_length=settings.INVAR_OCR_CHECK_LENGTH):
    ocr = str(ocr)
    assert check_length == 1 or check_length == 2

    return ocr[:-check_length]


def verify(ocr, check_length=settings.INVAR_OCR_CHECK_LENGTH):
    ocr = str(ocr)
    assert check_length == 1 or check_length == 2

    if baluhn_verify(ocr):
        if check_length == 1:
            return True
        elif check_length == 2 and str(len(ocr)) == ocr[-2]:
            return True
    return False
