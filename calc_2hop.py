########### Python 2.7 #############
import httplib, urllib, base64
import core_2hop, app_2hop
import time
import json
import sys, os, signal



########### sub_layer #############
def problem_0(id1, id2, n1, n2):
    ans = []
    t1 = core_2hop.getdata(n1)["entities"][0]
    t2 = core_2hop.getdata(n2)["entities"][0]

    ans += app_2hop.e_id_auid_id(id1, id2, t1, t2)
    ans += app_2hop.e_id_fcjid_id(id1, id2, t1, t2)
    ans += app_2hop.e_id_id_id(id1, id2, t1, t2)
    return ans

def problem_1(id1, id2, n1, n2):
    pass

def problem_2(id1, id2, n1, n2):
    pass

def problem_3(id1, id2, n1, n2):
    pass




########### main_layer #############
def calc(id1, id2, problem_type):
    #Type [id, id]
    if (problem_type == 0):
        return problem_0(id1, id2, "id1_paper", "id2_paper")

    #Type [id, auid]
    if (problem_type == 1):
        return problem_1(id1, id2, "id1_paper", "id2_author")

    #Type [auid, id]
    if (problem_type == 2):
        return problem_2(id1, id2, "id1_author", "id2_paper")

    #Type [auid, auid]
    if (problem_type == 3):
        return problem_3(id1, id2, "id1_author", "id2_author")

    return []

def main(id1, id2):
    problem_type = core_2hop.check_probleam_type(id1, id2)

    if (problem_type == -1): return []

    final_ans = calc(id1, id2, problem_type)
    print final_ans
    return final_ans

########### debug_layer #############
if __name__ == '__main__':
    #print calc(2147152072,189831743,0)
    #print core_2hop.auid_to_id(2077695977)
    main(2147152072,189831743)
    os.kill(os.getpid(), signal.SIGKILL)
