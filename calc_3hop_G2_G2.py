#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_utils

'''
Q1 = G2,G2:
1 ? G2->G1->G2->G2: Id -> (F/C/J AND RId) <- Id' (intersecting F/C/J)
2 V G2->G2->G1->G2: Id -> (RId AND F/C/J) <- Id' (intersecting F/C/J)
3 V G2->G2->G2->G2: Id -> (RId AND RId') <- Id' (intersecting RId)
4 V G2->G2->G3->G2: Id -> (RId AND AuId) <- Id' (intersecting AuId)
5 V G2->G3->G2->G2: Id -> (AuId AND RId) <- Id' (intersecting AuId)
    Interval results:
    Id1_FCJ, Id1_RId_FCJ, Id1_RId, Id1_RId_AuId, Id1_AuId
    Id2_RId_FCJ, Id2_FCJ, Id2_RId_RId, Id2_AuId, Id2_RId_AuId
'''

ret_list_3hop_1 = []
ret_list_3hop_2 = []
ret_list_3hop_3 = []
ret_list_3hop_4 = []
ret_list_3hop_5 = []

def G2_G2_1(entity1, entity2, num1, num2):
    # G2->G1->G2->G2: Id -> (F/C/J AND RId) <- Id' (intersecting F/C/J)
    # not possible to get all edges from left to right...
    return

def G2_G2_2(entity1, entity2, num1, num2):
    # G2->G2->G1->G2: Id -> (RId AND F/C/J) <- Id' (intersecting F/C/J)
    ret_list = []

    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_FCJ = {}
    for RId in Id1_RId:
        RId_FCJ = calc_3hop_utils.FCJ_by_IdEntity(calc_3hop_utils.send_request( expr=('Id=%s' % str(RId)) ))
        for method_id in RId_FCJ:
            if Id1_RId_FCJ.has_key(method_id) == False:
                Id1_RId_FCJ[method_id] = []
            Id1_RId_FCJ[method_id].append(RId)
    Id2_FCJ = calc_3hop_utils.FCJ_by_IdEntity(entity2)

    FCJ_intersection = list(set(Id1_RId_FCJ.keys()).intersection(set(Id2_FCJ)))

    for method_id in FCJ_intersection:
        for RId in Id1_RId_FCJ[method_id]:
            ret_list.append([num1, RId, method_id, num2])
    
    print "G2_G2_2 finished"
    return ret_list

def G2_G2_3(entity1, entity2, num1, num2):
    # G2->G2->G2->G2: Id -> (RId AND RId') <- Id' (intersecting RId)
    ret_list = []

    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_RId = {}
    for old_RId in Id1_RId:
        RId_RId = calc_3hop_utils.send_request(expr=('Id=%s' % str(old_RId)))["entities"][0]["RId"]
        for new_RId in RId_RId:
            if Id1_RId_RId.has_key(new_RId) == False:
                Id1_RId_RId[new_RId] = []
            Id1_RId_RId[new_RId].append(old_RId)

    for new_RId in Id1_RId_RId.keys():
        final_RId_list = calc_3hop_utils.send_request(expr=('Id=%s' % str(new_RId)))["entities"][0]["RId"]
        for final_RId in final_RId_list:
            if final_RId == num2:
                for Id1_RId in Id1_RId_RId[new_RId]:
                    ret_list.append([num1, Id1_RId, new_RId, num2])
    print "G2_G2_3 finished"
    return ret_list

def G2_G2_4(entity1, entity2, num1, num2):
    # G2->G2->G3->G2: Id -> (RId AND AuId) <- Id' (intersecting AuId)
    ret_list = []

    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_AuId = {}
    for RId in Id1_RId:
        RId_AuId = [AA_elem["AuId"] for AA_elem in calc_3hop_utils.send_request(expr=('Id=%s' % str(RId)))["entities"][0]["AA"]]
        for AuId in RId_AuId:
            if Id1_RId_AuId.has_key(AuId) == False:
                Id1_RId_AuId[AuId] = []
            Id1_RId_AuId[AuId].append(RId)
    Id2_AuId = [AA_elem["AuId"] for AA_elem in entity2["entities"][0]["AA"]]

    AuId_intersection = list(set(Id1_RId_AuId.keys()).intersection(set(Id2_AuId)))

    for AuId in AuId_intersection:
        for RId in Id1_RId_AuId[AuId]:
            ret_list.append([num1, RId, AuId, num2])
    print "G2_G2_4 finished"
    return ret_list

def G2_G2_5(entity1, entity2, num1, num2):
    # G2->G3->G2->G2: Id -> (AuId AND RId) <- Id' (intersecting AuId)
    ret_list = []

    Id1_AuId = [AA_elem["AuId"] for AA_elem in entity1["entities"][0]["AA"]]
    Id1_AuId_Id = {}
    for AuId in Id1_AuId:
        AuId_Id = [entity["Id"] for entity in calc_3hop_utils.send_request(expr=('Composite(AA.AuId=%s)' % str(AuId)))["entities"]]
        for new_Id in AuId_Id:
            if Id1_AuId_Id.has_key(new_Id) == False:
                Id1_AuId_Id[new_Id] = []
            Id1_AuId_Id[new_Id].append(AuId)

    for new_Id in Id1_AuId_Id.keys():
        final_RId_list = calc_3hop_utils.send_request(expr=('Id=%s' % str(new_Id)))["entities"][0]["RId"]
        for final_RId in final_RId_list:
            if final_RId == num2:
                for Id1_AuId in Id1_AuId_Id[new_Id]:
                    ret_list.append([num1, Id1_AuId, new_Id, num2])
    print "G2_G2_5 finished"
    return ret_list

def wrapper_3hop_2(entity1, entity2, num1, num2):
    global ret_list_3hop_2
    ret_list_3hop_2 = G2_G2_2(entity1, entity2, num1, num2)

def wrapper_3hop_3(entity1, entity2, num1, num2):
    global ret_list_3hop_3
    ret_list_3hop_3 = G2_G2_3(entity1, entity2, num1, num2)

def wrapper_3hop_4(entity1, entity2, num1, num2):
    global ret_list_3hop_4
    ret_list_3hop_4 = G2_G2_4(entity1, entity2, num1, num2)

def wrapper_3hop_5(entity1, entity2, num1, num2):
    global ret_list_3hop_5
    ret_list_3hop_5 = G2_G2_5(entity1, entity2, num1, num2)

def G2_G2(entity1, entity2, num1, num2):
    '''
    Id1_FCJ, Id1_RId_FCJ, Id1_RId, Id1_RId_AuId, Id1_AuId
    Id2_RId_FCJ, Id2_FCJ, Id2_RId_RId, Id2_AuId, Id2_RId_AuId
    '''
    print "G2_G2"
    ret_list = []

    t_hop3_2 = threading.Thread(target=wrapper_3hop_2,args=(entity1, entity2, num1, num2))
    t_hop3_2.start()
    t_hop3_3 = threading.Thread(target=wrapper_3hop_3,args=(entity1, entity2, num1, num2))
    t_hop3_3.start()
    t_hop3_4 = threading.Thread(target=wrapper_3hop_4,args=(entity1, entity2, num1, num2))
    t_hop3_4.start()
    t_hop3_5 = threading.Thread(target=wrapper_3hop_5,args=(entity1, entity2, num1, num2))
    t_hop3_5.start()

    t_hop3_2.join()
    t_hop3_3.join()
    t_hop3_4.join()
    t_hop3_5.join()

    return ret_list_3hop_2 + ret_list_3hop_3 + ret_list_3hop_4 + ret_list_3hop_5
