# -*- coding: utf-8 -*-
from apisync.http import QueryString

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

from unittest import TestCase
from unittest.mock import patch


class TestQueryString(TestCase):
    def test_when_filters_is_none(self):
        subject = QueryString()
        assert_equal(str(subject), "")


    def test_when_filters_is_not_none(self):
        subject = QueryString(filters={
            'metadata': {
                'customer_id': "abc",
                'second_key': "xyz",
            }
        })
        assert_equal(str(subject), "filter[metadata][customer-id]=abc&filter[metadata][second-key]=xyz")

    def test_when_including_attrs_many_levels_deep(self):
        deep_filter = {
            'level1': {
              'level2': {
                'level3': {
                  'level4': {
                    'key': "abc",
                  }
                }
              }
            }
        }
        subject = QueryString(filters=deep_filter)
        assert_equal(str(subject), "filter[level1][level2][level3][level4][key]=abc")

    def test_when_including_metadata_and_another_attribute(self):
        filters = {
            'application_id': 'app_id',
            'metadata': {
                'customer_id': "abc",
                'second_key': "xyz",
            }
        }
        subject = QueryString(filters=filters)
        assert_equal(str(subject), "filter[application-id]=app_id&filter[metadata][customer-id]=abc&filter[metadata][second-key]=xyz")
