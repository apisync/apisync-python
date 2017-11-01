# -*- coding: utf-8 -*-
from apisync.http import Url

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

from unittest import TestCase
from unittest.mock import patch


class TestUrl(TestCase):
    def test_when_host_is_passed_in(self):
        subject = Url('resource', id=None, filters={}, options={})
        subject.options["host"] = "http://custom-host"

        assert_equal(str(subject), "http://custom-host/resource")

    def test_when_host_is_not_passed_in(self):
        subject = Url('resource', id=None, filters={}, options={})

        assert_equal(str(subject), "https://api.apisync.io/resource")

    def test_returns_the_final_url_with_dasherized_resource(self):
        subject = Url('inventory_items')
        assert_equal(str(subject), "https://api.apisync.io/inventory-items")

    def test_when_id_is_present(self):
        subject = Url('resource', id="uuid", filters={}, options={})
        assert_equal(str(subject), "https://api.apisync.io/resource/uuid")

    def test_when_id_is_not_present(self):
        subject = Url('resource', id=None, filters={}, options={})
        assert_equal(str(subject), "https://api.apisync.io/resource")

    def test_query_string(self):
        filters = {
            'metadata': {
                'customer_id': "abc"
            }
        }
        subject = Url('resource', id=None, filters=filters, options={})
        assert_equal(str(subject), "https://api.apisync.io/resource?filter[metadata][customer-id]=abc")
