#!/usr/bin/env python3

from optparse import OptionParser

def parseCommandLineArguments():      
    parser = OptionParser()

    parser.add_option("--amount", type="float", dest="amount")
    parser.add_option("--input_currency", type="str", dest="inputCurrency")
    parser.add_option("--output_currency", type="str", dest="outputCurrency")

    # Optional
    parser.add_option("--noCache", action="store_false", dest="useCache", default=True)
    parser.add_option("--diagnostic", action="store_true", dest="showDiagnosticData", default=False)
    
    options, a = parser.parse_args()

    if not options.amount:
        parser.error("argument '--amount' is required")

    if not options.inputCurrency:
        parser.error("argument '--input_currency' is required")

    return options
        
