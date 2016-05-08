#!/usr/bin/python
import httplib, urllib, base64
import json

'''
G1 = F.FId/C.CId/J.JId
G2 = Id
G3 = AA.AuId
G4 = AA.AfId

G1 <-> G2 <-> G3 <-> G4
       |^
       ||

(Try to give some trivial answers)

Q1 = G2,G2:
    G2->G1->G2->G2: Id -> (F/C/J AND RId) <- Id' (intersecting F/C/J)
  V G2->G2->G1->G2: Id -> (RId AND F/C/J) <- Id' (intersecting F/C/J)
    G2->G2->G2->G2: Id -> (RId AND RId') <- Id' (intersecting RId)
    G2->G2->G3->G2: Id -> (RId AND AuId) <- Id' (intersecting AuId)
    G2->G3->G2->G2: Id -> (AuId AND RId) <- Id' (intersecting AuId)
    Interval results:
    Id1_FCJ, Id1_RId_FCJ, Id1_RId, Id1_RId_AuId, Id1_AuId
    Id2_RId_FCJ, Id2_FCJ, Id2_RId_RId, Id2_AuId, Id2_RId_AuId

Q2 = G2,G3:
    G2->G1->G2->G3: Id -> (F/C/J AND Id') <- AuId (intersecting F/C/J)
    G2->G2->G2->G3: Id -> (RId AND Id') <- AuId (intersecting RId)
    G2->G3->G2->G3: Id -> (AuId AND Id') <- AuId' (intersecting AuId)
    G2->G3->G4->G3: Id -> (AuId AND AfId) <- AuId' (intersecting AfId)
    Interval results:
    Id1_FCJ, Id1_RId, Id1_AuId, Id1_AuId_AfId
    AuId2_Id_FCJ, AuId2_Id_RId, AuId2_Id_AuId, AuId2_AfId

Q3 = G3,G2:
    G3->G2->G1->G2: AuId -> (Id AND F/C/J) <- Id' (intersecting F/C/J)
    G3->G2->G2->G2: AuId -> (Id AND RId) <- Id' (intersecting RId)
    G3->G2->G3->G2: AuId -> (Id AND AuId') <- Id' (intersecting AuId)
    G3->G4->G3->G2: AuId -> (AfId AND AuId') <- Id (intersecting AfId)
    Interval results:
    AuId1_Id_FCJ, AuId1_Id_RID, AuId1_id_AuId, AuId_AfId
    Id2_FCJ, Id2_RId, Id2_AuId, Id2_AuId_AfId

Q4 = G3,G3:
    G3->G2->G2->G3: AuId -> (Id AND Id') <- AuId' (intersecting RId)
    Interval results:
    AuId1_Id
    AuId2_Id_RId
'''

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
    
def G2_G2(entity1, entity2, num1, num2):
    '''
    Id1_FCJ, Id1_RId_FCJ, Id1_RId, Id1_RId_AuId, Id1_AuId
    Id2_RId_FCJ, Id2_FCJ, Id2_RId_RId, Id2_AuId, Id2_RId_AuId
    '''
    print "G2_G2"
    ret_list = []

    # G2->G2->G1->G2: Id -> (RId AND F/C/J) <- Id' (intersecting F/C/J)
    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_FCJ = {}
    for RId in Id1_RId:
        RId_FCJ = FCJ_by_IdEntity(send_request( expr=('Id=%s' % str(RId)) ))
        for method_id in RId_FCJ:
            if Id1_RId_FCJ.has_key(method_id) == False:
                Id1_RId_FCJ[method_id] = []
            Id1_RId_FCJ[method_id].append(RId)
    Id2_FCJ = FCJ_by_IdEntity(entity2)

    FCJ_intersection = list(set(Id1_RId_FCJ.keys()).intersection(set(Id2_FCJ)))

    for method_id in FCJ_intersection:
        for RId in Id1_RId_FCJ[method_id]:
            ret_list.append([num1, RId, method_id, num2])

    # G2->G2->G3->G2: Id -> (RId AND AuId) <- Id' (intersecting AuId)
    Id1_RId_AuId = {}
    for RId in Id1_RId:
        RId_AuId = [AA_elem["AuId"] for AA_elem in send_request(expr=('Id=%s' % str(RId)))["entities"][0]["AA"]]
        for AuId in RId_AuId:
            if Id1_RId_AuId.has_key(AuId) == False:
                Id1_RId_AuId[AuId] = []
            Id1_RId_AuId[AuId].append(RId)
    Id2_AuId = [AA_elem["AuId"] for AA_elem in entity2["entities"][0]["AA"]]

    AuId_intersection = list(set(Id1_RId_AuId.keys()).intersection(set(Id2_AuId)))

    for AuId in AuId_intersection:
        for RId in Id1_RId_AuId[AuId]:
            ret_list.append([num1, RId, AuId, num2])

    return ret_list

def G2_G3(entity1, entity2, num1, num2):
    print "G2_G3"
    return [[1,2,3,4]]

def G3_G2(entity1, entity2, num1, num2):
    print "G3_G2"
    return [[1,2,3,4]]

def G3_G3(entity1, entity2, num1, num2):
    '''
        AuId1_Id_RId
        AuId2_Id
    '''
    ret_list = []
    print "G3_G3"

    # G3->G2->G2->G3: AuId -> (Id AND Id') <- AuId' (intersecting RId)
    AuId1_Id = [entity["Id"] for entity in entity1["entities"]]
    AuId2_Id = [entity["Id"] for entity in entity2["entities"]]
    AuId1_Id_RId = {}
    for Id in AuId1_Id:
        Id_RId = send_request(expr=('Id=%s' % str(Id)))["entities"][0]["RId"]
        for RId in Id_RId:
            if AuId1_Id_RId.has_key(RId) == False:
                AuId1_Id_RId[RId] = []
            AuId1_Id_RId[RId].append(Id)

    RId_intersection = list(set(AuId1_Id_RId.keys()).intersection(set(AuId2_Id)))

    for RId in RId_intersection:
        for Id in AuId1_Id_RId[RId]:
            ret_list.append([num1, Id, RId, num2])
    
    return ret_list

def calc(num1, num2):
    entity1 = send_request(expr=('Id=%s' % str(num1)))
    entity2 = send_request(expr=('Id=%s' % str(num2)))
    
    if len(entity1["entities"]) == 0 or len(entity2["entities"]) == 0:
        return []

    if entity1["entities"][0].has_key("AA"):
        if entity2["entities"][0].has_key("AA"):
            return G2_G2(entity1, entity2, num1, num2)
        else:
            return G2_G3(entity1, send_request(expr=('Composite(AA.AuId=%s)' % str(num2))), 
                num1, num2)
    else:
        if entity2["entities"][0].has_key("AA"):
            return G3_G2(send_request(expr=('Composite(AA.AuId=%s)' % str(num1))), entity2, 
                num1, num2)
        else:
            return G3_G3(send_request(expr=('Composite(AA.AuId=%s)' % str(num1))), 
                send_request(expr=('Composite(AA.AuId=%s)' % str(num2))), 
                num1, num2)
    
if __name__ == '__main__':
    #num1 = 2133990480 #Id
    #num2 = 2126237948 #AuId
    #num1 = 2133990480
    #num2 = 2133990480
    print calc(2126237948, 2126237948)