#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_utils

'''
Q2 = G2,G3:
    G2->G1->G2->G3: Id -> (F/C/J AND Id') <- AuId (intersecting F/C/J)
    G2->G2->G2->G3: Id -> (RId AND Id') <- AuId (intersecting RId)
    G2->G3->G2->G3: Id -> (AuId AND Id') <- AuId' (intersecting AuId)
    G2->G3->G4->G3: Id -> (AuId AND AfId) <- AuId' (intersecting AfId)
    Interval results:
    Id1_FCJ, Id1_RId, Id1_AuId, Id1_AuId_AfId
    AuId2_Id_FCJ, AuId2_Id_RId, AuId2_Id_AuId, AuId2_AfId
'''

ret_list_3hop_G2_G3_1 = []
ret_list_3hop_G2_G3_2 = []
ret_list_3hop_G2_G3_3 = []
ret_list_3hop_G2_G3_4 = []

def G2_G3_1(entity1, entity2, num1, num2, reverse_out):
    # G2->G1->G2->G3: Id -> (F/C/J AND Id') <- AuId (intersecting F/C/J)
    global ret_list_3hop_G2_G3_1

    Id1_FCJ = calc_3hop_utils.FCJ_by_IdEntity(entity1)
    AuId_Id2 = [entity["Id"] for entity in entity2["entities"]]
    AuId_Id2_FCJ = {}
    for i in range(len(AuId_Id2)):
        calc_3hop_utils.send_request({"expr":('Id=%d' % AuId_Id2[i]), "target":("G2_G3_1_AuId_Id2_%d" % i)})
    for i in range(len(AuId_Id2)):
        Id2 = AuId_Id2[i]
        Id2_FCJ = calc_3hop_utils.FCJ_by_IdEntity(calc_3hop_utils.getdata("G2_G3_1_AuId_Id2_%d" % i))
        for method_id in Id2_FCJ:
            if AuId_Id2_FCJ.has_key(method_id) == False:
                AuId_Id2_FCJ[method_id] = []
            AuId_Id2_FCJ[method_id].append(Id2)

    FCJ_intersection = list(set(AuId_Id2_FCJ.keys()).intersection(set(Id1_FCJ)))

    for method_id in FCJ_intersection:
        for Id2 in AuId_Id2_FCJ[method_id]:
            if reverse_out == False:
                ret_list_3hop_G2_G3_1.append([num1, method_id, Id2, num2])
            else:
                ret_list_3hop_G2_G3_1.append([num2, Id2, method_id, num1])

    print "G2_G3_1 finished"

def G2_G3(entity1, entity2, num1, num2, reverse_out):
    '''
    Id1_FCJ, Id1_RId, Id1_AuId, Id1_AuId_AfId
    AuId2_Id_FCJ, AuId2_Id_RId, AuId2_Id_AuId, AuId2_AfId
    '''
    print "G2_G3"

    t_hop3_G2_G3_1 = threading.Thread(target=G2_G3_1,args=(entity1, entity2, num1, num2, reverse_out))
    t_hop3_G2_G3_1.start()

    t_hop3_G2_G3_1.join()

    return ret_list_3hop_G2_G3_1 + \
           ret_list_3hop_G2_G3_2 + \
           ret_list_3hop_G2_G3_3 + \
           ret_list_3hop_G2_G3_4