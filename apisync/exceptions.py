# -*- coding: utf-8 -*-

class Apisync:
    class Exception(Exception):
        pass

# List of exceptions. They are all inherited from Apisync::Exception
class UrlAndPayloadIdMismatch(Apisync.Exception):
    pass

class InvalidFilter(Apisync.Exception):
    pass

class TooManyRequests(Apisync.Exception):
    pass
