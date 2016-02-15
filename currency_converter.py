#!/usr/bin/env python3

from currency_symbol_code_identificator import CurrencySymbolCodeIdentificator
from exceptions import *
from argument_parser import parseCommandLineArguments
from available_currencies import getAvailableCurrencies
from yahoo_exchange_service import getExchangeRatesFromWebService
from currencies_rate_cache import writeRatesIntoCache, tryGetRatesFromCache
import json
import time

class CurrencyConverter:
    
    def __init__(self, useCache = True, showDiagnosticData = False):    
        self.useCache = useCache
        self.showDiagnosticData = showDiagnosticData
        self.availableCurrencies = getAvailableCurrencies()
        self.symbolTranslator = CurrencySymbolCodeIdentificator()   

    def convertIntoJson(self, inputCurrency, outputCurrencies, value):
        startTime = time.time()

        inputCurrency = self._translateInputCurrencyIntoValidCode(inputCurrency)
        outputCurrencies = self._translateOutputCurrenciesIntoValidCode(outputCurrencies)       
        rates, cachedData = self._getRates(inputCurrency, outputCurrencies)

        executionTime = time.time() - startTime
        diagnostic = self._createDiagnosticData(cachedData, executionTime)
        
        jsonResult = self._createJsonFromRates(inputCurrency, rates, value, diagnostic)
        return jsonResult

    def _getRates(self, inputCurrency, outputCurrencies):
        rates = None
        if self.useCache:
            cachedData = True
            rates = self._tryGetRatesFromCache(inputCurrency, outputCurrencies)
        if rates == None:
            cachedData = False
            rates = self._getExchangeRatesFromWebService(inputCurrency, outputCurrencies)
        return rates, cachedData

    def _getExchangeRatesFromWebService(self, inputCurrency, outputCurrencies):
        rates = getExchangeRatesFromWebService(inputCurrency, outputCurrencies)
        if self.useCache:
            writeRatesIntoCache(inputCurrency, rates)
        return rates

    def _createJsonFromRates(self, inputCurrency, rates, value, diagnosticData):
        result = {}

        if diagnosticData != None:
            result["diagnostic"] = diagnosticData
       
        result["input"] = {"amount": value, "currency": inputCurrency}
        result["output"] = {}
        for rate, converted in self._convertEach(rates, value):
            result["output"][rate.outputCurrency] = converted
        return result

    def _createDiagnosticData(self, cachedData, executionTime):
        if self.showDiagnosticData:
            return {
                "cachedData" : cachedData,
                "executionTime" : executionTime
            }
        return None

    def _convertEach(self, rates, value):
        for rate in rates:
            yield rate, rate.convert(value)

    def _tryGetRatesFromCache(self, inputCurrency, outputCurrencies):
        try:
            rates = tryGetRatesFromCache(inputCurrency, outputCurrencies)
            return rates
        except NotInCacheError as e:
            return None                  
 
    def _translateOutputCurrenciesIntoValidCode(self, currency):
        if currency != None:
            currency = [self._processCurrencyInput(currency)]
        else:
            currency = self.availableCurrencies
        return currency

    def _translateInputCurrencyIntoValidCode(self, currency):
        return self._processCurrencyInput(currency)

    def _processCurrencyInput(self, currencyInput):
        if currencyInput in self.availableCurrencies:
            return currencyInput
        currencyCode = self.symbolTranslator.translateToCode(currencyInput)
        if currencyCode == None:
            raise InvalidCurrency(currencyInput)
        return currencyCode

def main():
    args = parseCommandLineArguments()
    runConverter(args)

def runConverter(args):
    try:      
        converter = CurrencyConverter(useCache = args.useCache, showDiagnosticData = args.showDiagnosticData)
        jsonResult = converter.convertIntoJson(args.inputCurrency, args.outputCurrency, args.amount)
        print(json.dumps(jsonResult, indent=4, sort_keys=True))
    except InvalidCurrency as e:
        _printJsonError(e)
    except HTTPPageNotAvailableError as e:
        _printJsonError(e)
    except UnexpectedJsonFormatError as e:
        _printJsonError(e)
    except MissingRequiredDataError as e:
        _printJsonError(e)
    except Exception as e:
        print(e)
        _printJsonError("Yups. Someting unexpected happend :-(")

def _printJsonError(errorMsg):
    jsonError = {}
    jsonError['error'] = errorMsg
    print(json.dumps(jsonError, indent=4, sort_keys=True))
    
if __name__ == "__main__":
    main() 
