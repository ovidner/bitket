from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tickle.common.db.fields import NameField, SlugField, DescriptionField
from tickle.common.behaviors import NameSlugMixin
from tickle.common.models import Model
from tickle.organizers.models import Organizer
from tickle.products.models import Holding


class EventQuerySet(models.QuerySet):
    def holdings(self):
        return Holding.objects.filter(product__ticket_type__events__in=self)

    def visitors(self):
        return self.holdings().purchased().holders()

    def organizers(self):
        return Organizer.objects.filter(events__in = self).distinct()


@python_2_unicode_compatible
class MainEvent(Model):
    name = NameField()
    slug = SlugField(
        unique_with='organizer__slug',
        populate_from='name',
        editable=True)
    description = DescriptionField()

    organizer = models.ForeignKey(
        'organizers.Organizer',
        related_name='main_events',
        verbose_name=_('organizer'))

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('name',)
        unique_together = [
            ['organizer', 'name'],
            ['organizer', 'slug']
        ]

        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return self.name
