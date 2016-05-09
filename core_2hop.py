import httplib, urllib, base64
import threading
import json
from Queue import Queue

max_request_num = 200
datapool = {}
headers = {
    'Ocp-Apim-Subscription-Key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
}

def handle_request():
    while True:
        bundle = q.get()
        expr = bundle["expr"]
        target = bundle["target"]
        params_str = urllib.urlencode({
            'expr': str(expr),
            'count': '500',
            'offset': '0',
#            'orderby': 'Id:asc',
            'attributes': 'Id,F.FId,C.CId,J.JId,AA.AuId,RId'
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

        #print data
        #return json.loads(data)
        datapool[target] = json.loads(data)
        q.task_done()

def clear_datapool():
    global datapool
    datapool = {}

def getdata(datakey):
    q.join()
    return datapool[datakey]

def send_request(bundle):
    q.put(bundle)

def check_probleam_type(id1, id2):
    clear_datapool()
    send_request({"expr":('Id=%d' % id1), "target":"id1_paper"})
    send_request({"expr":('Id=%d' % id2), "target":"id2_paper"})
    send_request({"expr":('Composite(AA.AuId=%d)' % id1), "target":"id1_author"})
    send_request({"expr":('Composite(AA.AuId=%d)' % id2), "target":"id2_author"})

    t1 = getdata("id1_paper")
    t2 = getdata("id2_paper")

    if len(t1["entities"]) == 0 or len(t2["entities"]) == 0:
        return -1

    if t1["entities"][0].has_key("AA"):
        if t2["entities"][0].has_key("AA"):
            return 0
        else:
            #t2 = getdata("id2_author")
            return 1
    else:
        #t1 = getdata("id1_author")
        if t2["entities"][0].has_key("AA"):
            return 2
        else:
            #t2 = getdata("id2_author")
            return 3

###### Init Threading Pool ######
q = Queue(max_request_num * 2)
for i in range(max_request_num):
    t = threading.Thread(target=handle_request)
    t.start()
