# -*- coding: utf-8 -*-
import ssl

from django.conf import settings

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError


# Ugly hack due to Kobra sucking balls. See http://stackoverflow.com/a/32651967
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':RC4-SHA'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += ':RC4-SHA'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


API_URL = 'https://kobra.ks.liu.se/students/api.json'
API_ACCEPTED_PARAMS = (
    'liu_id',
    'email',
    'personal_number',
    'rfid_number',
    'barcode_number',
)


class StudentNotFound(Exception):
    pass


class Unauthorized(Exception):
    pass


class KobraAdapter(HTTPAdapter):
    def __init__(self):
        super(KobraAdapter, self).__init__()

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1
        super(KobraAdapter, self).init_poolmanager(*args, **kwargs)


class KobraClient(object):
    """
    A dead simple API client to KOBRA.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (settings.KOBRA_USER, settings.KOBRA_KEY)
        self.session.mount('https://kobra.ks.liu.se', KobraAdapter())

    def get_student(self, timeout=5.0, **data):
        """
        Calls the API and gets a student by **one** (1) of these parameters at a time:
        :param liu_id: LiU-ID (e.g. johec890)
        :param email: Email address (e.g. johec890@student.liu.se)
        :param personal_number: Personal identification number (e.g. 860421-0000)
        :param rfid_number: LiU card number (NFC/RFID, e.g. 3479871166)
        :param barcode_number: LiU card number (barcode/magnet, e.g. 975226854847805)
        :return: A dictionary with student data.
        """
        if len(data) != 1 or not any(i in API_ACCEPTED_PARAMS for i in data.keys()):
            # Raises a TypeError if called with other than exactly 1 argument or with other parameter than the ones
            # accepted.
            raise TypeError('Called with invalid argument(s) and/or wrong number of arguments.')

        response = self.session.post(API_URL, data=data, timeout=timeout)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Unauthorized('Invalid credentials.')
        elif response.status_code == 404:
            raise StudentNotFound
        else:
            raise HTTPError(('HTTP %s error.' % response.status_code), response=response)
