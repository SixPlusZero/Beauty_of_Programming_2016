########### Python 2.7 #############
import httplib, urllib, base64, core_1hop, os, signal
def problem_0(id1, id2, n1, n2):
    t1 = core_1hop.getdata(n1)["entities"][0]
    for rid in t1["RId"]:
        if (rid == id2):
            return 1
    return 0

def problem_1(id1, id2, n1, n2):
    t1 = core_1hop.getdata(n1)["entities"][0]
    if (not t1.has_key("AA")): return 0
    t1 = t1['AA']
    for aa in t1:
        if (aa['AuId'] == id2):
            return 1
    return 0

def problem_2(id1, id2, n1, n2):
    print id1, id2, n1, n2
    return problem_1(id2, id1, n2, n1)

def problem_3(id1, id2, n1, n2):
    return 0

#############################################################
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

    return 0




####################################
def main(id1, id2):
    problem_type = core_1hop.check_probleam_type(id1, id2)
    print "problem_type", problem_type
    if (problem_type == -1): return []
    stage_ans = calc(id1, id2, problem_type)
    print "Stage Ans for 1hop:", stage_ans
    if (stage_ans == 1):
        return [[id1, id2]]
    else:
        return []
if __name__ == '__main__':
    #print main(2251253715, 2180737804)
    #main(2147152072,189831743) #type0
    #main(2133990480,2126237948) #type1
    main(2251253715, 2180737804) #type2
    #main(2171035091, 2294309805) #type3
    os.kill(os.getpid(), signal.SIGKILL)
