#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_utils

'''
Q2 = G2,G3:
  V G2->G1->G2->G3: Id -> (F/C/J AND Id') <- AuId (intersecting F/C/J)
  
  V 
    G2->G2->G2->G3: Id -> (RId AND Id') <- AuId (intersecting RId)
    G3->G2->G2->G2: Id -> (RId AND Id') <- AuId (intersecting RId)
  
  V G2->G3->G2->G3: Id -> (AuId AND Id') <- AuId' (intersecting AuId)
  V G2->G3->G4->G3: Id -> (AuId AND AfId) <- AuId' (intersecting AfId)
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
    ret_list_3hop_G2_G3_1 = []

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

def G2_G3_2_2to3(entity1, entity2, num1, num2):
    # G2->G2->G2->G3: Id -> (RId AND Id') <- AuId (intersecting RId)
    global ret_list_3hop_G2_G3_2
    ret_list_3hop_G2_G3_2 = []

    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_RId = {}
    for i in range(len(Id1_RId)):
        calc_3hop_utils.send_request({"expr":('Id=%d' % Id1_RId[i]), "target":("G2_G3_2_RId_RId_%d" % i)})
    for i in range(len(Id1_RId)):
        old_RId = Id1_RId[i]
        RId_RId = calc_3hop_utils.getdata("G2_G3_2_RId_RId_%d" % i)["entities"][0]["RId"]
        for new_RId in RId_RId:
            if Id1_RId_RId.has_key(new_RId) == False:
                Id1_RId_RId[new_RId] = []
            Id1_RId_RId[new_RId].append(old_RId)

    AuId2_Id = [entity["Id"] for entity in entity2["entities"]]

    Id_intersection = list(set(Id1_RId_RId.keys()).intersection(set(AuId2_Id)))

    for Id in Id_intersection:
        for RId in Id1_RId_RId[Id]:
            ret_list_3hop_G2_G3_2.append([num1, RId, Id, num2])
    print "G2_G3_2_2223 finished"

def G2_G3_2_3to2(entity1, entity2, num1, num2):
    # G3->G2->G2->G2: Id -> (RId AND Id') <- AuId (intersecting RId)
    global ret_list_3hop_G2_G3_2
    ret_list_3hop_G2_G3_2 = []
    
    AuId_Id = [entity["Id"] for entity in entity1["entities"]]
    AuId_Id_RId = {}
    for i in range(len(AuId_Id)):
        calc_3hop_utils.send_request({"expr":('Id=%d' % AuId_Id[i]), "target":("G2_G3_2_Id_RId_%d" % i)})
    calc_3hop_utils.send_request({"expr":('RId=%d' % num2), "target":"G2_G3_2_Id_RingId"})
    for i in range(len(AuId_Id)):
        Id = AuId_Id[i]
        Id_RId = calc_3hop_utils.getdata("G2_G3_2_Id_RId_%d" % i)["entities"][0]["RId"]
        for RId in Id_RId:
            if AuId_Id_RId.has_key(RId) == False:
                AuId_Id_RId[RId] = []
            AuId_Id_RId[RId].append(Id)

    Id_RingId = [entity["Id"] for entity in calc_3hop_utils.getdata("G2_G3_2_Id_RingId")["entities"]]
    Id_intersection = list(set(AuId_Id_RId.keys()).intersection(set(Id_RingId)))

    for Id in Id_intersection:
        for RId in AuId_Id_RId[Id]:
            ret_list_3hop_G2_G3_2.append([num1, RId, Id, num2])
    print "G2_G3_2_3222 finished"

def G2_G3_3(entity1, entity2, num1, num2, reverse_out):
    # G2->G3->G2->G3: Id -> (AuId AND Id') <- AuId' (intersecting AuId)
    global ret_list_3hop_G2_G3_3
    ret_list_3hop_G2_G3_3 = []

    Id1_AuId1 = [AA_elem["AuId"] for AA_elem in entity1["entities"][0]["AA"]]
    Id1_AuId1_Id = {}
    for i in range(len(Id1_AuId1)):
        calc_3hop_utils.send_request(
            {"expr":('Composite(AA.AuId=%d)' % Id1_AuId1[i]), "target":("G2_G3_3_AuId_Id_%d" % i)})
    for i in range(len(Id1_AuId1)):
        AuId = Id1_AuId1[i]
        AuId_Id = [entity["Id"] for entity in calc_3hop_utils.getdata("G2_G3_3_AuId_Id_%d" % i)["entities"]]
        for new_Id in AuId_Id:
            if Id1_AuId1_Id.has_key(new_Id) == False:
                Id1_AuId1_Id[new_Id] = []
            Id1_AuId1_Id[new_Id].append(AuId)

    AuId2_Id2 = [entity["Id"] for entity in entity2["entities"]]
    Id_intersection = list(set(Id1_AuId1_Id.keys()).intersection(set(AuId2_Id2)))

    for Id2 in Id_intersection:
        for AuId in Id1_AuId1_Id[Id2]:
            if reverse_out == False:
                ret_list_3hop_G2_G3_3.append([num1, AuId, Id2, num2])
            else:
                ret_list_3hop_G2_G3_3.append([num2, Id2, AuId, num1])
    print "G2_G3_3 finished"

def G2_G3_4(entity1, entity2, num1, num2, reverse_out):
    # G2->G3->G4->G3: Id -> (AuId AND AfId) <- AuId' (intersecting AfId)
    global ret_list_3hop_G2_G3_4
    ret_list_3hop_G2_G3_4 = []

    Id_AuId1 = [AA_elem["AuId"] for AA_elem in entity1["entities"][0]["AA"]]
    Id_AuId1_AfId = {}

    # default AfId
    #for AA_elem in entity1["entities"][0]["AA"]:
    #    if Id_AuId1_AfId.has_key(AA_elem["AfId"]) == False:
    #        Id_AuId1_AfId[AA_elem["AfId"]] = []
    #    Id_AuId1_AfId[AA_elem["AfId"]].append(AA_elem["AuId"])
    # search more AfId
    for i in range(len(Id_AuId1)):
        calc_3hop_utils.send_request(
            {"expr":('Composite(AA.AuId=%d)' % Id_AuId1[i]), "target":("G2_G3_4_AuId_Id_%d" % i)})
    for i in range(len(Id_AuId1)):
        AuId = Id_AuId1[i]
        entity_list = calc_3hop_utils.getdata("G2_G3_4_AuId_Id_%d" % i)["entities"]
        for entity in entity_list:
            for AA_elem in entity["AA"]:
                if AA_elem.has_key("AfId"):
                    if Id_AuId1_AfId.has_key(AA_elem["AfId"]) == False:
                        Id_AuId1_AfId[AA_elem["AfId"]] = []
                    Id_AuId1_AfId[AA_elem["AfId"]].append(AA_elem["AuId"])

    AuId2_AfId = []

    for entity in entity2["entities"]:
        for AA_elem in entity["AA"]:
            if AA_elem["AuId"] == num2:
                if AA_elem.has_key("AfId"):
                    AuId2_AfId.append(AA_elem["AfId"])
    
    AfId_intersection = list(set(Id_AuId1_AfId.keys()).intersection(set(AuId2_AfId)))

    for AfId in AfId_intersection:
        for AuId in Id_AuId1_AfId[AfId]:
            if reverse_out == False:
                ret_list_3hop_G2_G3_4.append([num1, AuId, AfId, num2])
            else:
                ret_list_3hop_G2_G3_4.append([num2, AfId, AuId, num1])
    print "G2_G3_4 finished"
    
def G2_G3(entity1, entity2, num1, num2, reverse_out):
    '''
    Id1_FCJ, Id1_RId, Id1_AuId, Id1_AuId_AfId
    AuId2_Id_FCJ, AuId2_Id_RId, AuId2_Id_AuId, AuId2_AfId
    '''
    print "G2_G3"

    t_hop3_G2_G3_1 = threading.Thread(target=G2_G3_1,args=(entity1, entity2, num1, num2, reverse_out))
    t_hop3_G2_G3_1.start()
    if reverse_out == False:
        t_hop3_G2_G3_2 = threading.Thread(target=G2_G3_2_2to3,args=(entity1, entity2, num1, num2))
    else:
        t_hop3_G2_G3_2 = threading.Thread(target=G2_G3_2_3to2,args=(entity2, entity1, num2, num1))
    t_hop3_G2_G3_2.start()
    t_hop3_G2_G3_3 = threading.Thread(target=G2_G3_3,args=(entity1, entity2, num1, num2, reverse_out))
    t_hop3_G2_G3_3.start()
    t_hop3_G2_G3_4 = threading.Thread(target=G2_G3_4,args=(entity1, entity2, num1, num2, reverse_out))
    t_hop3_G2_G3_4.start()

    t_hop3_G2_G3_1.join(150)
    t_hop3_G2_G3_2.join(0)
    t_hop3_G2_G3_3.join(0)
    t_hop3_G2_G3_4.join(0)

    return calc_3hop_utils.unique_list(ret_list_3hop_G2_G3_1) + \
           calc_3hop_utils.unique_list(ret_list_3hop_G2_G3_2) + \
           calc_3hop_utils.unique_list(ret_list_3hop_G2_G3_3) + \
           calc_3hop_utils.unique_list(ret_list_3hop_G2_G3_4)