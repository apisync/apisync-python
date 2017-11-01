# -*- coding: utf-8 -*-
import requests
import json

from .http import Url, QueryString
from .exceptions import TooManyRequests, UrlAndPayloadIdMismatch, InvalidFilter

from .helpers import merge_dicts, hyphenize


class Apisync:
    VERSION = "0.1.4"

    def __init__(self, api_key=None):
        self.api_key = api_key

        if not api_key:
            raise AttributeError("missing keyword: api_key")

    def __getattr__(self, name):
        #def _method(*args, **kwargs):
        #    options = merge_dicts({'api_key': self.api_key}, kwargs)
        #    return Resource(name, options)
        #return _method
        return Resource(name, {'api_key': self.api_key})


class HttpClient:
    VERSION_PREFIX = ""

    HEADER = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }

    def __init__(self, resource_name, options={}, requests_lib=requests):
        self.resource_name = resource_name
        self.options = options
        self.requests = requests_lib

    def post(self, data={}, headers={}):
        return self.wrap_response(self.requests.post(
            self.url(), json={'data': self.payload_from_data(data)},
                headers=merge_dicts(self.header, headers)))

    def put(self, id=None, data={}, headers={}):
        if data["id"] != id:
            raise UrlAndPayloadIdMismatch()

        return self.wrap_response(self.requests.put(
            self.url(id=id),
            json={'data': self.payload_from_data(data)},
            headers=merge_dicts(self.header, headers)
        ))

    def get(self, id=None, filters=None, headers={}):
        if filters is None or type(filters) is not dict:
            raise InvalidFilter()

        return self.wrap_response(self.requests.get(
            self.url(id=id, filters=filters),
            headers=merge_dicts(self.header, headers)
        ))

    def url(self, id=None, filters=None):
        url = Url(resource_name=self.resource_name, id=id, filters=filters, options=self.options)
        return str(url)

    @property
    def header(self):
        final = HttpClient.HEADER
        if "api_key" in self.options:
            final = merge_dicts(final, {"Authorization": "ApiToken %s" % self.options["api_key"]})
        return final

    def payload_from_data(self, data):
        transformed_payload = {}
        for key, value in data.items():
            if type(value) is dict:
                transformed_payload[key] = self.payload_from_data(value)
            else:
                transformed_payload[hyphenize(key)] = value
        return transformed_payload

    def wrap_response(self, response):
        print(response.text)
        if response.status_code == 429:
            raise TooManyRequests()
        else:
            return response


class Resource:
    def __init__(self, name, options, client=None):
        self.name = name
        self.options = options
        self.client = client if client else HttpClient(resource_name=self.name, options=self.options)

    # Saves a resource.
    #
    # When the resource has an id in `data`, a `PUT` request is done. Otherwise
    # a `POST` takes place.
    #
    def save(self, data):
        data["type"] = hyphenize(self.name)

        headers = {}
        if "headers" in data:
            headers = data["headers"].copy()
            del data["headers"]
        if "id" in data:
            return self.put(data, headers=headers)
        else:
            return self.post(data, headers=headers)

    # Returns all resources that match the conditions passed in.
    #
    # 1. To find a resource by its id:
    #
    #   get(id: 'customer-id')
    #
    # 2. To find a resource by a column value
    #
    #   get(filters: {column_name: 'customer-id' }})
    #
    def get(self, conditions):
        return self.client.get(
            id=conditions.get("id", None),
            filters=conditions.get("filters", {}),
            headers=conditions.get("headers", {})
        )

    def post(self, data, headers={}):
        return self.client.post(
            data=data,
            headers=headers
        )

    def put(self, data, headers={}):
        return self.client.put(
            id=data["id"],
            data=data,
            headers=headers
        )
