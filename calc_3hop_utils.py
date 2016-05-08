#!/usr/bin/python
import httplib, urllib, base64
import json
import threading

headers = {
    'Ocp-Apim-Subscription-Key': 'f7cc29509a8443c5b3a5e56b0e38b5a6',
}

def send_request(
    expr='Id=0',
    count='100',
    offset='0',
    orderby='Id:asc',
    attributes='Id,F.FId,C.CId,J.JId,AA.AuId,AA.AfId,RId'):
    params_str = urllib.urlencode({
        'expr': str(expr),
        'count': str(count),
        'offset': str(offset),
        'orderby': str(orderby),
        'attributes': str(attributes)
    })
    data = []
    try:
        conn = httplib.HTTPSConnection('oxfordhk.azure-api.net')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params_str, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return json.loads(data)

def FCJ_by_IdEntity(entity):
    Id_FCJ = []
    if entity["entities"][0].has_key("F"):
        Id_FCJ += [F_elem["FId"] for F_elem in entity["entities"][0]["F"]]
    if entity["entities"][0].has_key("C"):
        Id_FCJ.append(entity["entities"][0]["C"]["CId"])
    if entity["entities"][0].has_key("J"):
        Id_FCJ.append(entity["entities"][0]["J"]["JId"])
    return Id_FCJ

