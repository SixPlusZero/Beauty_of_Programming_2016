########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
}

def send_request(params):
    try:
        conn = httplib.HTTPSConnection('oxfordhk.azure-api.net')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data

def check_id_id(id1, id2):
    params = urllib.urlencode({
        # Request parameters
        'expr': 'Id=%d' % (id1),
        'model': 'latest',
        'count': '1',
#        'offset': '0',
#        'orderby': 'CC:desc',
        'attributes': 'RId',
    })
    dataset = eval(send_request(params))["entities"]
    if (len(dataset) == 0): return 0
    RIdList = dataset[0]["RId"]
    if (len(RIdList) == 0): return 0
    for key in RIdList:
        if (key == id2): return 1
    return 0

def check_id_auid(id1, id2):
    params = urllib.urlencode({
        # Request parameters
        'expr': 'Id=%d' % (id1),
        'model': 'latest',
        'count': '1',
#        'offset': '0',
#        'orderby': 'CC:desc',
        'attributes': 'AA.AuId',
    })
    dataset = eval(send_request(params))["entities"]
    if (len(dataset) == 0): return 0
    AuIdList = dataset[0]["AA"]
    if (len(AuIdList) == 0): return 0
    for key in AuIdList:
        if (key["AuId"] == id2): return 1
    return 0


####################################
def calc(id1, id2):
    ans = check_id_id(id1, id2) or check_id_auid(id1, id2) or check_id_auid(id2, id1)
    if (ans == 1):
        return [[id1, id2]]
    else:
        return []

if __name__ == '__main__':
    print calc(1, 2)
