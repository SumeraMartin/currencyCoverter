#!/usr/bin/env python3

from exceptions import NotInCacheError
from exchange_rate import ExchangeRate
from cache_files import *
import os
import time

VALID_CACHE_TIME = 60 * 10

def writeRatesIntoCache(inputCurrency, exchangeRates):
    if cacheFileExist(inputCurrency):
        _rewriteExistFile(inputCurrency, exchangeRates)
    else:
        _writeToNewFile(inputCurrency, exchangeRates)

def tryGetRatesFromCache(inputCurrency, outputCurrencies):
    if not cacheFileExist(inputCurrency):
        raise NotInCacheError()
    return _getCachedRates(inputCurrency, outputCurrencies)
    
def _getCachedRates(inputCurrency, outputCurrencies):
    rates = _getAllRatesFromFile(inputCurrency)
    rates = _filterInvalidDateRates(rates)
    rates = _filterNotDesiredRates(rates, outputCurrencies)
    if not _ratesContainsAllDesiredCurrencies(rates, outputCurrencies):
        raise NotInCacheError()
    return rates

def _rewriteExistFile(inputCurrency, newRates):
    rates = _getAllRatesFromFile(inputCurrency)       
    rates = _filterInvalidDateRates(rates)
    rates = _filterNotDesiredRates(rates, newRates)
    _writeToNewFile(inputCurrency, rates + newRates)

def _writeToNewFile(inputCurrency, exchangeRates):
    with openCacheFile(inputCurrency, "w") as file:
        for rate in exchangeRates:
            rate.writeToFileWithTimeStamp(file)

def _getAllRatesFromFile(inputCurrency):
    rates = []
    with openCacheFile(inputCurrency, 'r') as file:
        for line in file:
            currency, rate, time = line.split()
            rate = ExchangeRate(inputCurrency, currency, rate, validUntil = time)
            rates.append(rate)
    return rates
    
def _filterInvalidDateRates(rates):
    return [rate for rate in rates if rate.isValid()]

def _filterNotDesiredRates(rates, outputCurrencies):
    return [rate for rate in rates if rate.outputCurrency in outputCurrencies]

def _ratesContainsAllDesiredCurrencies(rates, requiredCurrencies):
    return all(_ratesContainsCurrency(rates, requiredCurrency) for requiredCurrency in requiredCurrencies)

def _ratesContainsCurrency(rates, currency):
    return any(currency == rate.outputCurrency for rate in rates)    
