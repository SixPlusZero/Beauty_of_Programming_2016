#!/usr/bin/python
import httplib, urllib, base64
import json
import threading
import calc_3hop_G2_G2
import calc_3hop_G2_G3
import calc_3hop_G3_G3
import calc_3hop_utils

'''
G1 = F.FId/C.CId/J.JId
G2 = Id
G3 = AA.AuId
G4 = AA.AfId

G1 <-> G2 <-> G3 <-> G4
       |^
       ||
'''

def calc(num1, num2):
    calc_3hop_utils.clear_datapool()

    calc_3hop_utils.send_request({"expr":('Id=%d' % num1), "target":"entity1"})
    calc_3hop_utils.send_request({"expr":('Id=%d' % num2), "target":"entity2"})
    calc_3hop_utils.send_request({"expr":('Composite(AA.AuId=%d)' % num1), "target":"newentity1"})
    calc_3hop_utils.send_request({"expr":('Composite(AA.AuId=%d)' % num2), "target":"newentity2"})
    
    entity1 = calc_3hop_utils.getdata("entity1")
    entity2 = calc_3hop_utils.getdata("entity2")
    
    if len(entity1["entities"]) == 0 or len(entity2["entities"]) == 0:
        return []

    if entity1["entities"][0].has_key("AA"):
        if entity2["entities"][0].has_key("AA"):
            return calc_3hop_G2_G2.G2_G2(entity1, entity2, num1, num2)
        else:
            entity2 = calc_3hop_utils.getdata("newentity2")
            return calc_3hop_G2_G3.G2_G3(entity1, entity2, num1, num2, reverse_out=False)
    else:
        entity1 = calc_3hop_utils.getdata("newentity1")
        if entity2["entities"][0].has_key("AA"):
            return calc_3hop_G2_G3.G2_G3(entity2, entity1, num2, num1, reverse_out=True)
        else:
            entity2 = calc_3hop_utils.getdata("newentity2")
            return calc_3hop_G3_G3.G3_G3(entity1, entity2, num1, num2)
    
if __name__ == '__main__':
    #num1 = 2133990480 #Id
    #num2 = 2126237948 #AuId
    #num1 = 2133990480
    #num2 = 2133990480
    # 2251253715, 2180737804
    print calc(2332023333, 2310280492)