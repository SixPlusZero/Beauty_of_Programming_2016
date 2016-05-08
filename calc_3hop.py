#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_G2_G2
import calc_3hop_utils

'''
G1 = F.FId/C.CId/J.JId
G2 = Id
G3 = AA.AuId
G4 = AA.AfId

G1 <-> G2 <-> G3 <-> G4
       |^
       ||

(Try to give some trivial answers)

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
  V G3->G2->G2->G3: AuId -> (Id AND Id') <- AuId' (intersecting RId)
    Interval results:
    AuId1_Id
    AuId2_Id_RId
'''

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
        Id_RId = calc_3hop_utils.send_request(expr=('Id=%s' % str(Id)))["entities"][0]["RId"]
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
    entity1 = calc_3hop_utils.send_request(expr=('Id=%s' % str(num1)))
    entity2 = calc_3hop_utils.send_request(expr=('Id=%s' % str(num2)))
    
    if len(entity1["entities"]) == 0 or len(entity2["entities"]) == 0:
        return []

    if entity1["entities"][0].has_key("AA"):
        if entity2["entities"][0].has_key("AA"):
            return calc_3hop_G2_G2.G2_G2(entity1, entity2, num1, num2)
        else:
            return G2_G3(entity1, calc_3hop_utils.send_request(expr=('Composite(AA.AuId=%s)' % str(num2))), 
                num1, num2)
    else:
        if entity2["entities"][0].has_key("AA"):
            return G3_G2(calc_3hop_utils.send_request(expr=('Composite(AA.AuId=%s)' % str(num1))), entity2, 
                num1, num2)
        else:
            return G3_G3(calc_3hop_utils.send_request(expr=('Composite(AA.AuId=%s)' % str(num1))), 
                calc_3hop_utils.send_request(expr=('Composite(AA.AuId=%s)' % str(num2))), 
                num1, num2)
    
if __name__ == '__main__':
    #num1 = 2133990480 #Id
    #num2 = 2126237948 #AuId
    #num1 = 2133990480
    #num2 = 2133990480
    print calc(2133990480, 2133990480)