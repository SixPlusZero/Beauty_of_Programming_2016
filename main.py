#!/usr/bin/python
import sys
from sys import argv

import calc_1hop
import calc_2hop
import calc_3hop

import threading

ret_list_1hop = []
ret_list_2hop = []
ret_list_3hop = []

def wrapper_1hop(id1, id2):
	global ret_list_1hop
	ret_list_1hop = calc_1hop.main(id1, id2)

def wrapper_2hop(id1, id2):
	global ret_list_2hop
	ret_list_2hop = calc_2hop.main(id1, id2)


def wrapper_3hop(id1, id2):
	global ret_list_3hop
	ret_list_3hop = calc_3hop.calc(id1, id2)

def request(arg1, arg2):

    try:
        id1 = int(arg1)
        id2 = int(arg2)
    except ValueError:
        return 'Error: Illegal arguments!'
    t_1hop = threading.Thread(target=wrapper_1hop,args=(id1, id2))
    t_1hop.start()

    t_2hop = threading.Thread(target=wrapper_2hop,args=(id1, id2))
    t_2hop.start()

    t_3hop = threading.Thread(target=wrapper_3hop,args=(id1, id2))
    t_3hop.start()

    t_1hop.join()
    t_2hop.join()
    t_3hop.join()

    print "ret_list_1hop:"
    print ret_list_1hop
    print "ret_list_2hop:"
    print ret_list_2hop
    print "ret_list_3hop:"
    print ret_list_3hop

    return ret_list_1hop + ret_list_2hop + ret_list_3hop
