import unittest
import time

from available_currencies import writeCurrenciesIntoCacheFile
from currencies_rate_cache import writeRatesIntoCache
from currency_converter import CurrencyConverter
from exchange_rate import ExchangeRate
import json

class CurrencyConverterTest(unittest.TestCase):

    def setUp(self):
        validUntilTime = time.time() + 2
        
        writeCurrenciesIntoCacheFile(["EUR", "GBP", "USD"], validUntil = validUntilTime)      
        rateToEUR = ExchangeRate("USD", "EUR", 2.50, validUntil = validUntilTime)
        rateToGBP = ExchangeRate("USD", "GBP", 0.50, validUntil = validUntilTime)
        rateToUSD = ExchangeRate("USD", "USD", 1.00, validUntil = validUntilTime)
        writeRatesIntoCache("USD", [rateToEUR, rateToGBP, rateToUSD])
        
    def test(self):
        self.parseDataFromCache("USD", "EUR", 1, 2.5)
        self.parseDataFromCache("USD", "EUR", 2, 5)
        self.parseDataFromCache("USD", "GBP", 1, 0.5)
        self.parseDataFromCache("USD", "GBP", 2, 1)
        self.parseDataFromCache("USD", "USD", 1, 1)
        self.parseDataFromCache("USD", "USD", 2, 2)

        self.parseAllCurrencies("USD", 1, ["EUR", "GBP", "USD"], [2.5, 0.5, 1])

    def parseDataFromCache(self, inputCurrency, outputCurrency, value, expectedValue):
        converter = CurrencyConverter(useCache = True)
        jsonResult = converter.convertIntoJson(inputCurrency, outputCurrency, value)
        self.assertEqual(jsonResult['input']['amount'], value)
        self.assertEqual(jsonResult['input']['currency'], inputCurrency)
        self.assertEqual(jsonResult['output'][outputCurrency], expectedValue)

    def parseAllCurrencies(self, inputCurrency, value, expectedCurrencies, expectedValues):
        converter = CurrencyConverter(useCache = True)
        jsonResult = converter.convertIntoJson(inputCurrency, None, 1)

        self.assertEqual(jsonResult['input']['amount'], 1)
        self.assertEqual(jsonResult['input']['currency'], inputCurrency)

        for index in range(len(expectedCurrencies)):
            expectedCurrency = expectedCurrencies[index]
            expectedValue = expectedValues[index]
            self.assertEqual(jsonResult['output'][expectedCurrency], expectedValue)
