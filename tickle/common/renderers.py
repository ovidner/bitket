from __future__ import absolute_import, unicode_literals

from rest_framework import renderers
from rest_framework.response import Response

import qrcode
from six import BytesIO


class QrRenderer(renderers.BaseRenderer):
    media_type = 'image/png'
    format = 'qr'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        stream = BytesIO()
        qr_image = qrcode.make(data)
        qr_image.save(stream)
        response = stream.getvalue()
        stream.close()
        return response
