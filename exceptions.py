#!/usr/bin/env python3

class UnexpectedJsonFormatError(Exception):
    """
    Json is not in expected format, probably service has changed during time.
    """
    pass

class HTTPPageNotAvailableError(Exception):
    """
    Required webpage is not available. May be caused by no internet connection.
    """
    pass

class NotInCacheError(Exception):
    """
    Cache does not contains valid data.
    """
    pass

class InvalidCurrency(Exception):
    """
    Try to convert invalid currency
    """
    def __init__(self, currencyName):
        msg = "Invalid currency " + currencyName
        super(InvalidCurrency, self).__init__(msg)

class MissingRequiredDataError(IOError):
    """
    Missing required file
    """
    def __init__(self, fileName):
        msg = "Missing required file " + fileName
        super(MissingRequiredDataFormatError, self).__init__(msg)
