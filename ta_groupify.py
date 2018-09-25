#!/usr/bin/env python3
import json
import os
import re
import shutil

def get_ta_mail():
    slist = {
        'ta_name': "ta_mail",
    }
    ta_mailadress_list = "ta_mailadresses.json"

    with open(ta_mailadress_list,"w+") as file:
        json.dump(slist,file,indent=3)

    with open(ta_mailadress_list,"r") as file:
        tas = json.load(file)
    return tas


def divideByGroup(tas):
    submittedstudents = list(filter(lambda x: os.path.isdir("./" + x), os.listdir("./")))

    ta_counts = {}

    for ta in tas:
        ta_counts[ta] = 0

    for ta in tas:
        os.system("mkdir {}".format(ta))
        with open("./group_{}".format(ta),"r") as f:
            group = [x.rstrip() for x in f.readlines()]

        for student in group:
            found = [x for x in submittedstudents if student in x]
            if not found:
                print(student,"in group",ta,"not found")
                continue
            found = found[0]
            submittedstudents.remove(found)

            os.system("mv \"{}\" {}".format(found,ta))
            ta_counts[ta] += 1

    #Now just distribute to the lowest
    studentsleft = submittedstudents
    print()
    print("Randomly distributing",len(studentsleft),"students over the TA\'s")
    for student in studentsleft:
        lowta = min(ta_counts,key=ta_counts.get)
        shutil.move("./{}".format(student),"./{}".format(lowta))
        ta_counts[lowta] += 1
    print(ta_counts)

divideByGroup(get_ta_mail())
