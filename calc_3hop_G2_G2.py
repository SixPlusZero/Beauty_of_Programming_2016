#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_utils

'''
Q1 = G2,G2:
1 A G2->G1->G2->G2: Id -> (F/C/J AND RId) <- Id' (intersecting F/C/J)
2 V G2->G2->G1->G2: Id -> (RId AND F/C/J) <- Id' (intersecting F/C/J)
3 V G2->G2->G2->G2: Id -> (RId AND RId') <- Id' (intersecting RId)
4 V G2->G2->G3->G2: Id -> (RId AND AuId) <- Id' (intersecting AuId)
5 V G2->G3->G2->G2: Id -> (AuId AND RId) <- Id' (intersecting AuId)
    Interval results:
    Id1_FCJ, Id1_RId_FCJ, Id1_RId, Id1_RId_AuId, Id1_AuId
    Id2_RId_FCJ, Id2_FCJ, Id2_RId_RId, Id2_AuId, Id2_RId_AuId
'''

ret_list_3hop_G2_G2_1 = []
ret_list_3hop_G2_G2_2 = []
ret_list_3hop_G2_G2_3 = []
ret_list_3hop_G2_G2_4 = []
ret_list_3hop_G2_G2_5 = []

def G2_G2_1(entity1, entity2, num1, num2):
    # G2->G1->G2->G2: Id -> (F/C/J AND RId) <- Id' (intersecting F/C/J)
    global ret_list_3hop_G2_G2_1
    ret_list_3hop_G2_G2_1 = []

    Id1_FCJ = calc_3hop_utils.FCJ_by_IdEntity(entity1)
    calc_3hop_utils.send_request({"expr":('RId=%d' % num2), "target":"G2_G2_1_Id_RingId"}, 0)
    Id_RingId_entities = calc_3hop_utils.getdata("G2_G2_1_Id_RingId", 0)["entities"]
    
    for entity in Id_RingId_entities:
        RingId_FCJ = calc_3hop_utils.FCJ_by_IdEntity({"entities":[entity]})
        RingId = entity["Id"]
        FCJ_intersection = list(set(RingId_FCJ).intersection(set(Id1_FCJ)))
        for method_id in FCJ_intersection:
            ret_list_3hop_G2_G2_1.append([num1, method_id, RingId, num2])

    #print "G2_G2_1 finished"

def G2_G2_2(entity1, entity2, num1, num2):
    # G2->G2->G1->G2: Id -> (RId AND F/C/J) <- Id' (intersecting F/C/J)
    global ret_list_3hop_G2_G2_2
    ret_list_3hop_G2_G2_2 = []

    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_FCJ = {}

    for i in range(len(Id1_RId)):
        calc_3hop_utils.send_request({"expr":('Id=%d' % Id1_RId[i]), "target":("G2_G2_2_RId_FCJ_%d" % i)}, 1)
    for i in range(len(Id1_RId)):
        RId = Id1_RId[i]
        RId_FCJ = calc_3hop_utils.FCJ_by_IdEntity(calc_3hop_utils.getdata(("G2_G2_2_RId_FCJ_%d" % i), 1))
        for method_id in RId_FCJ:
            if Id1_RId_FCJ.has_key(method_id) == False:
                Id1_RId_FCJ[method_id] = []
            Id1_RId_FCJ[method_id].append(RId)
    Id2_FCJ = calc_3hop_utils.FCJ_by_IdEntity(entity2)

    FCJ_intersection = list(set(Id1_RId_FCJ.keys()).intersection(set(Id2_FCJ)))

    for method_id in FCJ_intersection:
        for RId in Id1_RId_FCJ[method_id]:
            ret_list_3hop_G2_G2_2.append([num1, RId, method_id, num2])
    
    #print "G2_G2_2 finished"

def G2_G2_3(entity1, entity2, num1, num2):
    # G2->G2->G2->G2: Id -> (RId AND RId') <- Id' (intersecting RId)
    global ret_list_3hop_G2_G2_3
    ret_list_3hop_G2_G2_3 = []

    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_RId = {}
    for i in range(len(Id1_RId)):
        calc_3hop_utils.send_request({"expr":('Id=%d' % Id1_RId[i]), "target":("G2_G2_3_RId_RId_%d" % i)}, 2)
    calc_3hop_utils.send_request({"expr":('RId=%d' % num2), "target":"G2_G2_3_Id_RingId"}, 2)
    for i in range(len(Id1_RId)):
        old_RId = Id1_RId[i]
        #try:
        RId_RId = calc_3hop_utils.getdata(("G2_G2_3_RId_RId_%d" % i), 2)["entities"][0]["RId"]
        for new_RId in RId_RId:
            if Id1_RId_RId.has_key(new_RId) == False:
                Id1_RId_RId[new_RId] = []
            Id1_RId_RId[new_RId].append(old_RId)
        #except:
            #continue

    Id_RingId = [entity["Id"] for entity in calc_3hop_utils.getdata("G2_G2_3_Id_RingId", 2)["entities"]]
    Id_intersection = list(set(Id1_RId_RId.keys()).intersection(set(Id_RingId)))

    for Id in Id_intersection:
        for RId in Id1_RId_RId[Id]:
            ret_list_3hop_G2_G3_3.append([num1, RId, Id, num2])    
    #print "G2_G2_3 finished"

def G2_G2_4(entity1, entity2, num1, num2):
    # G2->G2->G3->G2: Id -> (RId AND AuId) <- Id' (intersecting AuId)
    global ret_list_3hop_G2_G2_4
    ret_list_3hop_G2_G2_4 = []

    Id1_RId = entity1["entities"][0]["RId"]
    Id1_RId_AuId = {}

    for i in range(len(Id1_RId)):
        calc_3hop_utils.send_request({"expr":('Id=%d' % Id1_RId[i]), "target":("G2_G2_4_RId_AuId_%d" % i)}, 3)
    for i in range(len(Id1_RId)):
        RId = Id1_RId[i]
        #try:
        RId_AuId = [AA_elem["AuId"] for AA_elem in calc_3hop_utils.getdata(("G2_G2_4_RId_AuId_%d" % i), 3)["entities"][0]["AA"]]
        for AuId in RId_AuId:
            if Id1_RId_AuId.has_key(AuId) == False:
                Id1_RId_AuId[AuId] = []
            Id1_RId_AuId[AuId].append(RId)
        #except:
            #continue

    Id2_AuId = [AA_elem["AuId"] for AA_elem in entity2["entities"][0]["AA"]]

    AuId_intersection = list(set(Id1_RId_AuId.keys()).intersection(set(Id2_AuId)))

    for AuId in AuId_intersection:
        for RId in Id1_RId_AuId[AuId]:
            ret_list_3hop_G2_G2_4.append([num1, RId, AuId, num2])
    #print "G2_G2_4 finished"

def G2_G2_5(entity1, entity2, num1, num2):
    # G2->G3->G2->G2: Id -> (AuId AND RId) <- Id' (intersecting AuId)
    global ret_list_3hop_G2_G2_5
    ret_list_3hop_G2_G2_5 = []

    Id1_AuId = [AA_elem["AuId"] for AA_elem in entity1["entities"][0]["AA"]]
    Id1_AuId_Id = {}
    for i in range(len(Id1_AuId)):
        calc_3hop_utils.send_request(
            {"expr":('Composite(AA.AuId=%d)' % Id1_AuId[i]), "target":("G2_G2_5_AuId_Id_%d" % i)}, 4)
    calc_3hop_utils.send_request({"expr":('RId=%d' % num2), "target":"G2_G2_5_Id_RingId"}, 4)
    for i in range(len(Id1_AuId)):
        AuId = Id1_AuId[i]
        AuId_Id = [entity["Id"] for entity in calc_3hop_utils.getdata(("G2_G2_5_AuId_Id_%d" % i), 4)["entities"]]
        for new_Id in AuId_Id:
            if Id1_AuId_Id.has_key(new_Id) == False:
                Id1_AuId_Id[new_Id] = []
            Id1_AuId_Id[new_Id].append(AuId)

    Id_RingId = [entity["Id"] for entity in calc_3hop_utils.getdata("G2_G2_5_Id_RingId", 4)["entities"]]
    Id_intersection = list(set(Id1_AuId_Id.keys()).intersection(set(Id_RingId)))

    for Id in Id_intersection:
        for RId in Id1_AuId_Id[Id]:
            ret_list_3hop_G2_G3_5.append([num1, RId, Id, num2])    

    #print "G2_G2_5 finished"

def G2_G2(entity1, entity2, num1, num2):
    '''
    Id1_FCJ, Id1_RId_FCJ, Id1_RId, Id1_RId_AuId, Id1_AuId
    Id2_RId_FCJ, Id2_FCJ, Id2_RId_RId, Id2_AuId, Id2_RId_AuId
    '''
    #print "G2_G2"

    t_hop3_G2_G2_1 = threading.Thread(target=G2_G2_1,args=(entity1, entity2, num1, num2))
    t_hop3_G2_G2_1.start()
    t_hop3_G2_G2_2 = threading.Thread(target=G2_G2_2,args=(entity1, entity2, num1, num2))
    t_hop3_G2_G2_2.start()
    t_hop3_G2_G2_3 = threading.Thread(target=G2_G2_3,args=(entity1, entity2, num1, num2))
    t_hop3_G2_G2_3.start()
    t_hop3_G2_G2_4 = threading.Thread(target=G2_G2_4,args=(entity1, entity2, num1, num2))
    t_hop3_G2_G2_4.start()
    t_hop3_G2_G2_5 = threading.Thread(target=G2_G2_5,args=(entity1, entity2, num1, num2))
    t_hop3_G2_G2_5.start()

    t_hop3_G2_G2_1.join(0)
    t_hop3_G2_G2_2.join(0)
    t_hop3_G2_G2_3.join(0)
    t_hop3_G2_G2_4.join(0)
    t_hop3_G2_G2_5.join(60)

    '''
    print "ret_list_3hop_G2_G2_1"
    print calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_1)
    print "ret_list_3hop_G2_G2_2"
    print calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_2)
    print "ret_list_3hop_G2_G2_3"
    print calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_3)
    print "ret_list_3hop_G2_G2_4"
    print calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_4)
    print "ret_list_3hop_G2_G2_5"
    print calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_5)
    '''

    return calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_1) + \
           calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_2) + \
           calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_3) + \
           calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_4) + \
           calc_3hop_utils.unique_list(ret_list_3hop_G2_G2_5)