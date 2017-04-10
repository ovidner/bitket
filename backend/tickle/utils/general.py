from __future__ import absolute_import, unicode_literals


def get_nested_attr(obj, attr_list, default=None):
    obj = getattr(obj, attr_list.pop(0), default)
    if attr_list:
        return get_nested_attr(obj, attr_list, default)
    return obj


def get_dotted_attr(obj, attr, default=None):
    attr_list = attr.split('.')
    return get_nested_attr(obj, attr_list, default)


def get_double_underscore_attr(obj, attr, default=None):
    attr_list = attr.split('__')
    return get_nested_attr(obj, attr_list, default)


