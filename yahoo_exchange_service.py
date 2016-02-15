#!/usr/bin/python3.4

from exchange_rate import ExchangeRate
from exceptions import HTTPPageNotAvailableError
import urllib.request
import urllib.error
import json
import time

QUERY_PLACEHOLDER = "[QUERY]"
URL_WITHOUT_QUERY = "https://query.yahooapis.com/v1/public/yql?q=" + QUERY_PLACEHOLDER + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
QUERY_WITHOUT_PARAMS = "select * from yahoo.finance.xchange where pair in (%s)"

def getExchangeRatesFromWebService(inputCurrency, outputCurrencies):
    rates = []
        
    json = _getResponseJson(inputCurrency, outputCurrencies)
    count = json["query"]["count"]
    if count == 1:
        outputCurrency, rate = _parseRateValuesFromJson(json["query"]["results"]["rate"])
        rates.append(ExchangeRate(inputCurrency, outputCurrency, rate))
    else:
        for rateJson in json["query"]["results"]["rate"]:
            outputCurrency, rate = _parseRateValuesFromJson(rateJson)
            rates.append(ExchangeRate(inputCurrency, outputCurrency, rate))
        
    return rates

def _getResponseJson(inputCurrency, outputCurrencies):
    completeQuery = QUERY_WITHOUT_PARAMS % _createQueryParams(inputCurrency, outputCurrencies)
    urlFriendlyQuery = urllib.parse.quote_plus(completeQuery)
    completeURL = URL_WITHOUT_QUERY.replace(QUERY_PLACEHOLDER, urlFriendlyQuery)
    try:
        with urllib.request.urlopen(completeURL) as response:
            response = response.read().decode('utf8')
            return json.loads(response)
    except urllib.error.URLError as e:
        raise HTTPPageNotAvailableError(completeURL) from e

def _createQueryParams(inputCurrency, outputCurrencies):
    queryParams = ""
    for index, outputCurrency in enumerate(outputCurrencies):
        queryParams += "'" + inputCurrency + outputCurrency + "'"
        if index != len(outputCurrencies) - 1:
            queryParams += ","
    return queryParams

def _parseOutputCurrencyName(inputOutputName):
    """
    Name is in format 'XXXYYY',
    where 'XXX' is input currency and 'YYY' is output currency
    """
    return inputOutputName[3:]

def _parseRateValuesFromJson(rateJson):
    outputCurrency = _parseOutputCurrencyName(rateJson["id"])
    rate = rateJson["Rate"]
    return outputCurrency, rate

if __name__ == "__main__":
    rates = getExchangeRates("USD",["GBP", "BTC"])
    for rate in rates:
        print(rate.convert(10), rate.outputCurrency)

