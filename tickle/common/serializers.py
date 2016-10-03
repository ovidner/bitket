from __future__ import absolute_import, unicode_literals

from rest_framework import serializers
from rest_framework_expandable import ExpandableSerializerMixin

from tickle.common.utils.general import get_double_underscore_attr


class HyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    def __init__(self, *args, **kwargs):
        self._parent_lookups = kwargs.pop('parent_lookups', {})
        super(HyperlinkedRelatedField, self).__init__(*args, **kwargs)

    def use_pk_only_optimization(self):
        # This just gives us a load of problems. Disabled for now.
        return False

    def get_parent_lookups(self):
        return self._parent_lookups

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}

        for kwarg, orm_lookup in self.get_parent_lookups().iteritems():
            kwargs[kwarg] = get_double_underscore_attr(obj, orm_lookup)

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        """
        Return the object corresponding to a matched URL.

        Takes the matched URL conf arguments, and should return an
        object instance, or raise an `ObjectDoesNotExist` exception.
        """
        lookup_value = view_kwargs[self.lookup_url_kwarg]
        lookup_kwargs = {self.lookup_field: lookup_value}

        for kwarg, orm_lookup in self.get_parent_lookups().iteritems():
            lookup_kwargs[orm_lookup] = view_kwargs[kwarg]

        return self.get_queryset().get(**lookup_kwargs)


class HyperlinkedIdentityField(HyperlinkedRelatedField):
    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super(HyperlinkedIdentityField, self).__init__(view_name, **kwargs)


class HyperlinkedModelSerializer(ExpandableSerializerMixin, serializers.HyperlinkedModelSerializer):
    serializer_url_field = HyperlinkedIdentityField
    serializer_related_field = HyperlinkedRelatedField
