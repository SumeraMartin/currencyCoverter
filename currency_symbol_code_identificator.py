#!/usr/bin/python3.4

from cache_files import openDataFile
import json
import os

class CurrencySymbolCodeIdentificator:

    DATA_FILE_NAME = "currencies_symbols.data"

    def __init__(self):
        self._currenciesSymbols = dict()
        self._loadDataFromFile()

    def __contains__(self, key):
        return key in self._currenciesSymbols          
            
    def translateToCode(self, symbol):
        if symbol in self._currenciesSymbols:
            return self._currenciesSymbols[symbol]
        return None

    def _loadDataFromFile(self):      
        with openDataFile(self.DATA_FILE_NAME, 'r') as dataFile:
            data = dataFile.readlines()
            for currencyLine in data:
                currencyLine = currencyLine.split(' ')               
                code = currencyLine[0].strip()
                if len(currencyLine) == 2:
                    symbol = currencyLine[1].strip()
                    self._currenciesSymbols[symbol] = code
                
