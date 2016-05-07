########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
}

params = urllib.urlencode({
    # Request parameters
    'expr': 'Id=2077695977',
    'model': 'latest',
    'count': '100',
    'offset': '0',
    'orderby': 'CC:desc',
    'attributes': 'AA.AuId,AA.AuN,Id,Ti,RId',
})

def send_request(params):
    try:
        conn = httplib.HTTPSConnection('oxfordhk.azure-api.net')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data
####################################
def calc(num1, num2):
    return [[num1, num2]]
