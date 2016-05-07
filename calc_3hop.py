#!/usr/bin/python
import httplib, urllib, base64
import json

def calc(num1, num2):

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
    }

    params = urllib.urlencode({
        # Request parameters
        'expr': 'Composite(AA.AuN=\'aditya parameswaran\')',
        'model': 'latest',
        'count': '100',
        'offset': '0',
        'orderby': 'CC:desc',
        'attributes': 'Ti,AA.AuN,AA.AfN,Y,D,CC',
    })

    try:
        conn = httplib.HTTPSConnection('oxfordhk.azure-api.net')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return [[1,2,3,4]]

