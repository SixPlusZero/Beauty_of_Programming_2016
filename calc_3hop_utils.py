#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
from Queue import Queue

max_request_num = 200

datapool = {}

headers = {
    'Ocp-Apim-Subscription-Key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
}

def doWork():
    while True:
        bundle = q.get()
        
        expr = bundle["expr"]
        target = bundle["target"]
        
        attributes = 'Id,F.FId,C.CId,J.JId,AA.AuId,AA.AfId,RId,CC'
        if bundle.has_key("attributes"):
            attributes = bundle["attributes"]

        count = '1000000'
        if bundle.has_key("count"):
            count = bundle["count"]

        offset = '0'
        if bundle.has_key("offset"):
            offset = bundle["offset"]

        params_str = urllib.urlencode({
            'expr': expr,
            'count': count,
            'offset': offset,
#            'orderby': 'Id:asc',
            'attributes': attributes
        })
        data = []

        while True:
            try:
                conn = httplib.HTTPSConnection('oxfordhk.azure-api.net', timeout=10)
                conn.request("GET", "/academic/v1.0/evaluate?%s" % params_str, "{body}", headers)
                response = conn.getresponse()
                data = response.read()
                conn.close()
                break
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
                #print params_str
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

q = Queue(max_request_num * 3)
for i in range(max_request_num):
    t = threading.Thread(target=doWork)
    t.start()

def send_request(bundle):
    q.put(bundle)

def send_RId_request(RId, CC, attributes, target):
    idx = 0
    count = 1000
    ret_list = []
    while idx < CC:
        for_times = 0
        for i in range(max_request_num):
            send_request({"expr":('RId=%d' % RId), \
                          "target": "send_RId_request_" + str(i + idx) + target, \
                          "count": ("%d" % count), \
                          "offset": ("%d" % (i * count + idx)), \
                          "attributes": attributes})
            for_times += 1
            if (i + 1) * count + idx > CC:
                break
        for i in range(for_times):
            #print json.dumps(getdata("send_RId_request_" + str(i + idx) + target))
            ret_list += getdata("send_RId_request_" + str(i + idx) + target)["entities"]
        idx += for_times * count
    print "send_RId_request: %d times" % idx
    return ret_list

def unique_list(origin_list):
    new_list = []
    for elem in origin_list:
        if elem not in new_list:
            new_list.append(elem)
    return new_list
    