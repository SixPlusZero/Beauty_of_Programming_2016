#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_utils

'''
Q3 = G3,G2:
    G3->G2->G1->G2: AuId -> (Id AND F/C/J) <- Id' (intersecting F/C/J)
    G3->G2->G2->G2: AuId -> (Id AND RId) <- Id' (intersecting RId)
    G3->G2->G3->G2: AuId -> (Id AND AuId') <- Id' (intersecting AuId)
    G3->G4->G3->G2: AuId -> (AfId AND AuId') <- Id (intersecting AfId)
    Interval results:
    AuId1_Id_FCJ, AuId1_Id_RID, AuId1_id_AuId, AuId_AfId
    Id2_FCJ, Id2_RId, Id2_AuId, Id2_AuId_AfId
'''

def G3_G2(entity1, entity2, num1, num2):
    '''
    AuId1_Id_FCJ, AuId1_Id_RID, AuId1_id_AuId, AuId_AfId
    Id2_FCJ, Id2_RId, Id2_AuId, Id2_AuId_AfId
    '''
    #print "G3_G2"
    return [[1,2,3,4]]