from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tickle.common.db.fields import NameField, SlugField, DescriptionField
from tickle.common.behaviors import NameSlugMixin


class EventQuerySet(models.QuerySet):
    def holdings(self):
        return Holding.objects.filter(product__ticket_type__events__in=self)

    def visitors(self):
        return self.holdings().purchased().holders()


@python_2_unicode_compatible
class MainEvent(models.Model):
    name = NameField()
    slug = SlugField()
    description = DescriptionField()

    organizer = models.ForeignKey(
        'organizers.Organizer',
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
