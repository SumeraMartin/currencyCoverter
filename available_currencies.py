#!/usr/bin/env python3

from exceptions import UnexpectedJsonFormatError
from exceptions import HTTPPageNotAvailableError
from cache_files import *
import urllib.request
import urllib.error
import os, json, time

DATA_FILE_NAME = "available_currencies.data"
AVAILABLE_CURRENCIES_URL = "http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json"
CURRENCY_NAME_PREFIX = "USD/"
CURRENCY_CODE_LENGTH = 3
UPDATE_INTERVAL = 60 * 60 * 24 #One day

def getAvailableCurrencies():
    """
    Download and cache available currencies in json format,
    from 'finance.yahoo.com', which can be used as conversion currency.
    """
    if not _dataFileIsValid():
        currencies = _getCurrenciesFromWebpage()
        writeCurrenciesIntoCacheFile(currencies)
    else:
        currencies = _getCurrenciesFromCacheFile()
    return currencies

def writeCurrenciesIntoCacheFile(currencies, validUntil=None):
    with openCacheFile(DATA_FILE_NAME, 'w') as file:
        if validUntil == None:
            validUntil = time.time()
        file.write(str(validUntil) + "\n")
        for currency in currencies:
            file.write(currency + "\n")

def _dataFileIsValid():
    if not cacheFileExist(DATA_FILE_NAME):
        return False
    return not _fileContainsDataOlderThan(UPDATE_INTERVAL)
    
def _fileContainsDataOlderThan(updateInterval):
    with openCacheFile(DATA_FILE_NAME, 'r') as file:
        createDate = float(file.readline())
        if time.time() - createDate >= updateInterval:
            return True
    return False

def _getCurrenciesFromCacheFile():
    with openCacheFile(DATA_FILE_NAME, 'r') as file:
        currencies = []
        for line in file:
            line = line[:len(line) - 1]
            if len(line) == CURRENCY_CODE_LENGTH:
                currencies.append(line)
        return currencies
        
def _getCurrenciesFromWebpage():
    json = _downloadAvaiableCurrenciesJsonData()
    return _parseAvailableCurrenceis(json)

def _downloadAvaiableCurrenciesJsonData():
    try:
        with urllib.request.urlopen(AVAILABLE_CURRENCIES_URL) as response:
            response = response.read().decode('utf8')
    except urllib.error.URLError as e:
        excMsg = "Required webpage " + AVAILABLE_CURRENCIES_URL + " is not available"
        raise HTTPPageNotAvailableError(excMsg) from e 
    return json.loads(response)

def _parseAvailableCurrenceis(json):
    availableCurrencies = []
    try:
        resources = json["list"]["resources"]
        for res in resources:
            currencyName = res["resource"]["fields"]["name"]
            if _isValidCurrencyInUSDAgainstFormat(currencyName):
                currencyName = _trimRedudantPartOfCurrencyName(currencyName)
                availableCurrencies.append(currencyName)
            elif currencyName == "USD":
                availableCurrencies.append(currencyName)
    except KeyError as e:
        raise UnexpectedJsonFormatException("Json url source: " + AVAILABLE_CURRENCIES_URL) from e
    return availableCurrencies

def _trimRedudantPartOfCurrencyName(currencyName):
    return currencyName[4:]

def _isValidCurrencyInUSDAgainstFormat(currencyName):
    """ Format of currency is 'USD/GBP' """
    if not currencyName.startswith(CURRENCY_NAME_PREFIX):
        return False
    if not len(_trimRedudantPartOfCurrencyName(currencyName)) == CURRENCY_CODE_LENGTH:
        return False
    return True

if __name__ == "__main__":
    print(getAvailableCurrencies())
        
