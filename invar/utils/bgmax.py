# -*- coding: utf-8 -*-
import re
from datetime import date, datetime
from pytz import timezone
from parse import parse
from decimal import Decimal

from django.conf import settings


STARTING_RECORD = re.compile(r'^01BGMAX {15}(?P<version>\d{2})(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})(?P<microsecond>\d{6})(?P<code>[PT])\s*$', re.MULTILINE)
SECTION = re.compile(r'^05(?P<receiver_bg>\d{10})(?P<receiver_pg>[\d\s]{10})(?P<currency>\w{3}).*(?P<payments_raw>[\s\S]*?)\n150{19}(?P<receiver_clearing>\d{4})(?P<receiver_account>\d{12})(?P<deposit_year>\d{4})(?P<deposit_month>\d{2})(?P<deposit_day>\d{2})(?P<deposit_uid>\d{5})\d{18}\w{3}\d{8}(?P<deposit_type>[KDS ]).*', re.MULTILINE)
PAYMENT = re.compile(r'^20(?P<sender_bg>\d{10})(?P<reference>[\w\d\s]{25})(?P<amount>\d{18})(?P<reference_code>\d)(?P<payment_channel>\d)(?P<uid>\d{12})(?P<image>\d).*$', re.MULTILINE)


def _parse_starting_record(data):
    r = STARTING_RECORD.search(data).groupdict()

    return {
        'version': int(r['version']),
        'production': r['code'] == 'P',
        'creation_timestamp': datetime(
            int(r['year']),
            int(r['month']),
            int(r['day']),
            int(r['hour']),
            int(r['minute']),
            int(r['second']),
            int(r['microsecond']),
            timezone(settings.INVAR_BGMAX_TIMEZONE)
        )
    }


def _parse_payments(data):
    payments = []

    for payment in PAYMENT.finditer(data):
        gd = payment.groupdict()

        amount = Decimal(gd['amount'][:-2] + '.' + gd['amount'][-2:])

        reference_code = int(gd['reference_code'])

        if reference_code == 0 or reference_code == 1:
            reference = None
        else:
            reference = gd['reference'].lstrip(' ').rstrip(' ')

        payments.append({
            'amount': amount,
            'reference': reference,
            'reference_code': reference_code,
            'uid': gd['uid'],
            'payment_channel': int(gd['payment_channel']),
            'sender_bg': gd['sender_bg'].lstrip('0') or None,
            'image': gd['image'] == '1',
        })

    return payments


def _parse_sections(data):
    sections = []

    for section in SECTION.finditer(data):
        gd = section.groupdict()

        sections.append({
            'currency': gd['currency'],
            'deposit_uid': int(gd['deposit_uid']),
            'deposit_type': gd['deposit_type'].strip(' ') or None,
            'deposit_date': date(
                int(gd['deposit_year']),
                int(gd['deposit_month']),
                int(gd['deposit_day'])
            ),
            'receiver_bg': gd['receiver_bg'].lstrip('0'),
            'receiver_pg': gd['receiver_pg'].lstrip(' ').lstrip('0') or None,
            'receiver_clearing': gd['receiver_clearing'].lstrip('0'),
            'receiver_account': gd['receiver_account'].lstrip('0'),
            'payments': _parse_payments(gd['payments_raw'])
        })

    return sections


def parse_file(data):
    result = _parse_starting_record(data)
    result['sections'] = _parse_sections(data)

    return result
