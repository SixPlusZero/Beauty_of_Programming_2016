#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
from Queue import Queue

max_request_num = 300

datapool = {}

headers = {
    'Ocp-Apim-Subscription-Key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
}

def doWork():
    while True:
        bundle = q.get()
        
        expr = bundle["expr"]
        target = bundle["target"]
        params_str = urllib.urlencode({
            'expr': str(expr),
            'count': '2000',
            'offset': '0',
            'orderby': 'Id:asc',
            'attributes': 'Id,F.FId,C.CId,J.JId,AA.AuId,AA.AfId,RId'
        })
        data = []

        while True:
            try:
                conn = httplib.HTTPSConnection('oxfordhk.azure-api.net', timeout=5)
                conn.request("GET", "/academic/v1.0/evaluate?%s" % params_str, "{body}", headers)
                response = conn.getresponse()
                data = response.read()
                conn.close()
                break
            except Exception as e:
                #print("[Errno {0}] {1}".format(e.errno, e.strerror))
                print params_str
                continue

        #return json.loads(data)
        datapool[target] = json.loads(data)

        q.task_done()

def FCJ_by_IdEntity(entity):
    Id_FCJ = []
    if entity["entities"][0].has_key("F"):
        Id_FCJ += [F_elem["FId"] for F_elem in entity["entities"][0]["F"]]
    if entity["entities"][0].has_key("C"):
        Id_FCJ.append(entity["entities"][0]["C"]["CId"])
    if entity["entities"][0].has_key("J"):
        Id_FCJ.append(entity["entities"][0]["J"]["JId"])
    return Id_FCJ

def clear_datapool():
    global datapool
    datapool = {}

def getdata(datakey):
    q.join()
    return datapool[datakey]

q = Queue(max_request_num * 2)
for i in range(max_request_num):
    t = threading.Thread(target=doWork)
    t.start()

def send_request(bundle):
    q.put(bundle)

def unique_list(origin_list):
    new_list = []
    for elem in origin_list:
        if elem not in new_list:
            new_list.append(elem)
    return new_list
    