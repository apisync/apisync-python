# -*- coding: utf-8 -*-
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

from unittest import TestCase
from unittest.mock import patch

from apisync.core import Resource
import requests_mock


class TestHttpClient(TestCase):

    def setUp(self):
        self.options = {'host': 'host', 'api_key': 'api_key'}

    @patch('apisync.core.HttpClient')
    def test_save(self, HttpClient):
        http_client = HttpClient('inventory_items', self.options)
        subject = Resource('inventory_items', self.options, http_client)

        subject.save({
            'attributes': {
                'key': "value"
            },
            'headers': {
                'key': "value"
            }
        })

        subject.client.post.assert_called_with(
            data={'attributes': {'key': "value"}, 'type': "inventory-items"},
            headers={'key': "value"}
        )

    @patch('apisync.core.HttpClient')
    def test_save_with_id(self, HttpClient):
        http_client = HttpClient('inventory_items', self.options)
        subject = Resource('inventory_items', self.options, http_client)

        subject.save({
            'id': 'uuid',
            'attributes': {
                'key': "value"
            },
            'headers': {
                'key': "value"
            }
        })

        subject.client.put.assert_called_with(
            id='uuid',
            data={
                'id': 'uuid',
                'attributes': {
                    'key': "value"
                },
                'type': "inventory-items"
            },
            headers={'key': "value"}
        )

    @patch('apisync.core.HttpClient')
    def test_get_with_id(self, HttpClient):
        http_client = HttpClient('inventory_items', self.options)
        subject = Resource('inventory_items', self.options, http_client)

        subject.get({
            'id': 'uuid',
            'api_key': 'api_key',
            'filters': {
                'key': "value"
            },
            'headers': {
                'key': "value"
            }
        })

        subject.client.get.assert_called_with(
            id='uuid',
            filters={'key': "value"},
            headers={'key': "value"}
        )
