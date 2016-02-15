#!/usr/bin/python3.4

from decimal import Decimal, ROUND_HALF_UP
import time

class ExchangeRate:

    VALID_CACHE_TIME = 60 * 10

    def __init__(self, inputCurrency, outputCurrency, rating, validUntil = None):
        self.inputCurrency = inputCurrency
        self.outputCurrency = outputCurrency
        self.rating = float(rating)
        self.validUntil = validUntil

    def isValid(self):
        if self.validUntil == None:
            return False
        return time.time() - float(self.validUntil) < self.VALID_CACHE_TIME

    def convert(self, value):
        ratedValue = self.rating * value
        threeFloatingPointsValue = float("%.3f" % ratedValue)
        a = self._roundHalfUpWithTwoFloatingPoints(threeFloatingPointsValue)
        return float(a)

    def writeToFileWithTimeStamp(self, file):
        timestamp = self.validUntil
        if timestamp == None:           
            timestamp = time.time()
        file.write(self._createLineWithTimeStamp(timestamp) + "\n")

    def _createLineWithTimeStamp(self, time):
        return self.outputCurrency + " " + str(self.rating) + " " + str(time)

    def _roundHalfUpWithTwoFloatingPoints(self, value):
        """ Avoid banker's round and always round half up"""    
        dec = Decimal(str(value))
        roundedDec = dec.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        return float(roundedDec)

    def __repr__(self):
        return "[%s][%s][%f]" % (self.inputCurrency, self.outputCurrency, self.rating)
