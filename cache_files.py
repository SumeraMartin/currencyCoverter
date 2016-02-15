#!/usr/bin/env python3

from contextlib import contextmanager
from exceptions import MissingRequiredDataError
import os

CACHE_DIR_NAME = ".cache/"
DATA_DIR_NAME = "data/"

@contextmanager
def openCacheFile(fileName, fileOpenArg):
    _createCacheDirIfNotExist()
    try:
        file = open(_getCacheFilePath(fileName), fileOpenArg, encoding="utf8")
        yield file
    except IOError as e:
        raise IOError("Can't open/create file " + _getCacheFilePath(fileName))
    finally:
        file.close()

@contextmanager
def openDataFile(fileName, fileOpenArg):
    try:
        file = open( _getDataFilePath(fileName), fileOpenArg, encoding="utf8")
        yield file
    except IOError as e:
        raise MissingRequiredDataError(_getDataFilePath(fileName)) from e
    finally:
        file.close()

def cacheFileExist(fileName):
    return os.path.isfile(_getCacheFilePath(fileName))

def _getCacheFilePath(fileName):
    return CACHE_DIR_NAME + fileName

def _getDataFilePath(fileName):
    return DATA_DIR_NAME + fileName

def _createCacheDirIfNotExist():
    if not os.path.exists(CACHE_DIR_NAME):
        os.makedirs(CACHE_DIR_NAME)


