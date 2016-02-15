#!/usr/bin/env python3

import unittest

import sys
sys.path.append("..")

import os

from currency_symbol_code_identificator import CurrencySymbolCodeIdentificator

class CurrenciesIdentificatorTest(unittest.TestCase):

    def setUp(self):
        self.identificator = CurrencySymbolCodeIdentificator()
    
    def test(self):        
        self.existingSymbol("$", "USD")
        self.existingSymbol("£", "GBP")
        self.existingSymbol("CA$", "CAD")

    def existingSymbol(self, symbol, code):
        self.assertEqual(code, self.identificator.translateToCode(symbol))
