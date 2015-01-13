from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Material(models.Model):
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=16)

    def __str__(self):
        return '%s [%s]' % (self.name, self.unit)

    def total_amount(self):
        return self.entrymaterial_set.aggregate(amount=models.Sum('amount'))['amount']


@python_2_unicode_compatible
class MaterialRole(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EntryMaterial(models.Model):
    entry = models.ForeignKey('Entry')
    material = models.ForeignKey('Material')

    amount = models.DecimalField(max_digits=9, decimal_places=3)
    role = models.ForeignKey('MaterialRole')

    class Meta:
        ordering = ('entry', 'material', 'role')

    def __str__(self):
        return '%s: %s %s %s (%s)' % (self.entry.name, self.amount, self.material.unit, self.material.name, self.role.name)


@python_2_unicode_compatible
class EntryCustomMaterial(models.Model):
    entry = models.ForeignKey('Entry')
    material = models.CharField(max_length=256)

    amount = models.DecimalField(max_digits=9, decimal_places=3)
    unit = models.CharField(max_length=8)
    role = models.ForeignKey('MaterialRole')

    def __str__(self):
        return '%s: %s %s %s (%s)' % (self.entry.name, self.amount, self.unit, self.material, self.role.name)

@python_2_unicode_compatible
class EntryType(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    max_members = models.PositiveIntegerField()

    class Meta:
        ordering = ('max_members', 'name',)

    def __str__(self):
        return '%s (%s)' % (self.name, self.description)


@python_2_unicode_compatible
class Entry(models.Model):
    constellation = models.CharField(max_length=256, verbose_name=_('constellation'), help_text=_('E.g. <em>MPiRE</em>, <em>Grabbarna Grus</em>'))
    name = models.CharField(max_length=256, verbose_name=_('entry name'))
    type = models.ForeignKey('EntryType', related_name='entries', verbose_name=_('entry type'))
    members = models.PositiveIntegerField(default=10, verbose_name=_('number of members'))

    # Fult som stryk!
    primary_contact_name = models.CharField(max_length=256, verbose_name=_('name'))
    primary_contact_address = models.CharField(max_length=256, verbose_name=_('address'))
    primary_contact_postcode = models.CharField(max_length=6, verbose_name=_('postcode'))
    primary_contact_city = models.CharField(max_length=64, verbose_name=_('city'))
    primary_contact_phone = models.CharField(max_length=256, verbose_name=_('phone'))
    primary_contact_email = models.EmailField(verbose_name=_('email'))

    secondary_contact_name = models.CharField(max_length=256, verbose_name=_('name'))
    secondary_contact_address = models.CharField(max_length=256, verbose_name=_('address'))
    secondary_contact_postcode = models.CharField(max_length=6, verbose_name=_('postcode'))
    secondary_contact_city = models.CharField(max_length=64, verbose_name=_('city'))
    secondary_contact_phone = models.CharField(max_length=256, verbose_name=_('phone'))
    secondary_contact_email = models.EmailField(verbose_name=_('email'))

    width = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_('width'), help_text=_('Width in meters, in direction of movement.'))
    length = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_('length'), help_text=_('Length in meters, in direction of movement.'))
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_('height'), help_text=_('Height in meters.'))

    description = models.TextField(verbose_name=_('description'), help_text=_('Describe your idea! Maximum 500 words.'))
    spex_description = models.TextField(verbose_name=_('spex description'), help_text=_('Describe what will happen in, on and around your carriage! Music, theatre or anything else amusing? Maximum 500 words.'))
    other_information = models.TextField(blank=True, null=True, verbose_name=_('other information'), help_text=_('Want us to know something else?'))

    materials = models.ManyToManyField('Material', through='EntryMaterial')

    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

        unique_together = (('constellation', 'name'),)

    def __str__(self):
        return self.constellation

    def clean(self):
        errors = []

        if self.members > self.type.max_members:
            errors.append(ValidationError(_('Too many members for this entry type.')))

        if self.type.name == "Fribygge" and not (self.width and self.length and self.height):
            errors.append(ValidationError(_('Free build must have specified, valid dimensions.')))

        if errors:
            raise ValidationError(errors)