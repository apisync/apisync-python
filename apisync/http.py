# -*- coding: utf-8 -*-
from .helpers import flatten, hyphenize, merge_dicts, compact

from urllib.parse import urlparse


# Responsible for generating URLs
class Url:
    DEFAULT_HOST = "https://api.apisync.io"

    """
     - resource_name: a name in plural such as 'users', 'profiles' etc.
     - id: id of the resource that you're looking for
     - filters: these will define what's in the query string, such as
       'filter[application-id]=value'
     - options: allows you to pass options such 'host'. Accepted options are

       - host: a custom host for the URL, defaults to DEFAULT_HOST
    """
    def __init__(self, resource_name, id=None, filters=None, options={}):
        self.resource_name = resource_name
        self.id = id
        self.filters = filters

        self.options = merge_dicts({"host": None}, options)

    # to_s
    #
    # Takes a host, api_version, resource name and id and form the URL. Then
    # pass filters and other options into QueryString class which will return
    # whatever is after the `?` symbol.
    #
    # Returns a string such as
    #
    #    'https://api.apisync.io/inventory-items?filter[application-id]=abc'
    #
    # If there are no query strings, omits the `?`
    #
    #    'https://api.apisync.io/inventory-items'
    #
    def __str__(self):
        items = compact([self.host, self.api_version, self.normalized_resource_name, self.id])
        url = "/".join(items)
        url = self.remove_duplicated_slashes(url)
        return "?".join(compact([url, self.query_string]))

    @property
    def query_string(self):
        qs = str(QueryString(self.filters))
        return qs if qs != "" else None

    @property
    def api_version(self):
        from .core import HttpClient
        return HttpClient.VERSION_PREFIX

    @property
    def host(self):
        if "host" in self.options:
            if self.options["host"]:
                return self.options["host"]
        return Url.DEFAULT_HOST

    @property
    def normalized_resource_name(self):
        return hyphenize(self.resource_name)

    def remove_duplicated_slashes(self, url):
        parsed_url = urlparse(url)
        return url


class QueryString:
    def __init__(self, filters=None):
        self.filters = filters

    def __str__(self):
        return self.format_filters() if self.filters else ""

    # Takes a list of `[key]=value` strings and maps them adding `"filter"`
    # as prefix.
    #
    # Results in `filter[key]=value&filter[key2]=value2`.
    def format_filters(self):
        filter_list = list(map(lambda item: "filter%s" % item, flatten(self.recursive_brackets(self.filters))))
        return "&".join(filter_list)


    # Takes a hash such as
    #
    #   {
    #     field_one: 'value1',
    #     metadata: {
    #       field_two: "value2",
    #       field_three: "value3"
    #     }
    #   }
    #
    # and returns
    #
    #   [
    #     "[field-one]=value1",
    #     "[metadata][field-two]=value2",
    #     "[metadata][field-three]=value3"
    #   ]
    #
    # This can be used for creating filter querystrings.
    def recursive_brackets(self, filters, prefix=""):
        result = []
        for key, value in filters.items():
            key = hyphenize(key)
            if type(value) is dict:
                prefix = "%s[%s]" % (prefix, key)
                top_nodes = self.recursive_brackets(value, prefix)
                result.append(top_nodes)
            else:
                result.append("%s[%s]=%s" % (prefix, key, value))
        return result
