#!/usr/bin/python
import sys
from sys import argv

def request(arg1, arg2):

    try:
        id1 = int(arg1)
        id2 = int(arg2)
    except ValueError:
        return 'Error: Illegal arguments!'

    return [[id1, id2]]

