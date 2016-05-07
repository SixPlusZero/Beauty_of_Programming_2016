#!/usr/bin/python
import sys
from sys import argv
import calc_3hop

def request(arg1, arg2):

    ret_list = []

    try:
        id1 = int(arg1)
        id2 = int(arg2)
    except ValueError:
        return 'Error: Illegal arguments!'

    ret_list.append(calc_3hop.calc(id1, id2))

    return ret_list

