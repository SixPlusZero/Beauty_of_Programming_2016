#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_utils

'''
Q4 = G3,G3:
  V G3->G2->G2->G3: AuId -> (Id AND Id') <- AuId' (intersecting RId)
    Interval results:
    AuId1_Id
    AuId2_Id_RId
'''

ret_list_3hop_G3_G3_1 = []

def G3_G3_1(entity1, entity2, num1, num2):
    global ret_list_3hop_G3_G3_1
    ret_list_3hop_G3_G3_1 = []

    # G3->G2->G2->G3: AuId -> (Id AND Id') <- AuId' (intersecting RId)
    AuId1_Id = [entity["Id"] for entity in entity1["entities"]]
    AuId2_Id = [entity["Id"] for entity in entity2["entities"]]
    AuId1_Id_RId = {}
    for i in range(len(AuId1_Id)):
    	calc_3hop_utils.send_request({"expr":('Id=%d' % AuId1_Id[i]), "target":("G3_G3_Id_RId_%d" % i)})
    for i in range(len(AuId1_Id)):
    	Id = AuId1_Id[i]
        Id_RId = calc_3hop_utils.getdata("G3_G3_Id_RId_%d" % i)["entities"][0]["RId"]
        for RId in Id_RId:
            if AuId1_Id_RId.has_key(RId) == False:
                AuId1_Id_RId[RId] = []
            AuId1_Id_RId[RId].append(Id)

    RId_intersection = list(set(AuId1_Id_RId.keys()).intersection(set(AuId2_Id)))

    for RId in RId_intersection:
        for Id in AuId1_Id_RId[RId]:
            ret_list_3hop_G3_G3_1.append([num1, Id, RId, num2])
    print "G2_G3_3_3 finished"

def G3_G3(entity1, entity2, num1, num2):
    '''
    AuId1_Id
    AuId2_Id_RId
    '''
    print "G3_G3"
    ret_list = []

    t_hop3_G3_G3_1 = threading.Thread(target=G3_G3_1,args=(entity1, entity2, num1, num2))
    t_hop3_G3_G3_1.start()
    
    t_hop3_G3_G3_1.join(60)
    
    return calc_3hop_utils.unique_list(ret_list_3hop_G3_G3_1)