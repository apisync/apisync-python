# -*- coding: utf-8 -*-

def merge_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def flatten(nested_list):
    """Given a list, possibly nested to any level, return it flattened."""
    result = []
    for item in nested_list:
        if type(item) == type([]):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def compact(items):
    """Removes empty or None elements from lists"""
    return filter(lambda item: item is not None and len(item) > 0, items)

def hyphenize(value):
    return str(value).lower().replace("_", "-")
