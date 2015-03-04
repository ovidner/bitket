# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


class TemplatedEmail(EmailMultiAlternatives):
    def __init__(self, subject='', subject_template=None, body_template_html=None, context=None,
                 from_email=None, to=None, cc=None, bcc=None, connection=None, attachments=None, headers=None,
                 alternatives=None, tags=None):

        plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext

        if subject_template:
            rendered_subject = render_to_string(subject_template, context, plaintext_context)
        else:
            rendered_subject = subject

        rendered_body_html = render_to_string(body_template_html, context)

        super(TemplatedEmail, self).__init__(subject=rendered_subject, from_email=from_email, to=to, cc=cc, bcc=bcc,
                                             connection=connection, attachments=attachments, headers=headers,
                                             alternatives=alternatives)
        self.attach_alternative(rendered_body_html, 'text/html')
        self.tags = tags
