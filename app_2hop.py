########### Python 2.7 #############
import httplib, urllib, base64
import core_2hop, app_2hop
import time
import json
import sys, os, signal

def check_type(id1, id2, l1, l2, N, sN):
    if (not l1.has_key(N)): return []
    if (not l2.has_key(N)): return []

    list1 = l1[N]
    list2 = l2[N]
    ans = []
    if (not type(list1) is list):
        if (list1[sN] == list2[sN]):
            return [id1, list1[sN], id2]
        else:
            return []
    for i in list1:
        for j in list2:
            if (i[sN] == j[sN]):
                ans.append([id1, i[sN], id2])
    return ans


def e_id_auid_id(id1, id2, d1, d2):
    t1 = time.time()
    ans = []
    ans += check_type(id1, id2, d1, d2, 'AA', 'AuId')
    t2 = time.time()
    print "e_id_auid_id", t2 - t1, "sec(s)"
    return ans

def e_id_fcjid_id(id1, id2, d1, d2):
    t1 = time.time()
    ans = []
    ans += check_type(id1, id2, d1, d2, 'F', 'FId')
    ans += check_type(id1, id2, d1, d2, 'C', 'CId')
    ans += check_type(id1, id2, d1, d2, 'J', 'JId')
    t2 = time.time()
    print "e_id_fcj_id", t2 - t1, "sec(s)"
    return ans

def e_id_id_id(id1, id2, d1, d2):
    t1 = time.time()
    ans = []
    list_1h = d1['RId']
    len_1hop = len(list_1h)
    for w in list_1h:
        sub_ans = core_2hop.send_request({"expr":('Id=%d' % id1), "target":"id_id_id_%d" % w})
    for w in list_1h:
        w = core_2hop.getdata("id_id_id_%d" % w)
        if (not w.has_key("entities")): continue
        w = w["entities"][0]
        if (not w.has_key("RId")): continue
        w = w['RId']
        for ww in w:
            if (ww == id2):
                ans.append([id1, w, id2])
                break
    t2 = time.time()
    print "e_id_id_id", t2 - t1, "sec(s)"

    return ans
