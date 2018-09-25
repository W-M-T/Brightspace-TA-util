#!/usr/bin/env python3

import os
import re
from bs4 import BeautifulSoup

RE_HTML = "^.*\\.html$"
reg = re.compile(RE_HTML)

RE_USERS = "^Users:\\s*(\\d+)$"
reg_users = re.compile(RE_USERS)

RE_ENROLLED = "enrolled in (.*)$"
reg_enrollment = re.compile(RE_ENROLLED)

RE_CUSTOM_GROUP_NAME = "^Wercollegegr \\d (.+) \\w{2} \\d{1,2}\\.\\d{2}"
reg_custom = re.compile(RE_CUSTOM_GROUP_NAME)

zips = list(filter(lambda x : x, map(lambda x: reg.match(x), os.listdir())))

group_list = {}

problematic_users = []

ungrouped_users = []

for i in zips:
    with open(i.group(0)) as file:
        soup = BeautifulSoup(file.read(),'html.parser')
    usertable = soup.find(id="z_h")
    del(soup)
    group_row = usertable.find("tr", class_="d_gh").find_all("th")
    for th in group_row:
        found_name = th.find("label")
        found_amount = th.find(class_="ds_i")
        if found_name is not None:
            name = found_name.string
            parsed_amount = int(reg_users.match(found_amount.string).group(1))
            if name not in group_list:
                group_list[name] = (parsed_amount,[])
            else:
                group_list[name] = (group_list[name][0]+parsed_amount,group_list[name][1])

    user_rows = [x.parent for x in usertable.find_all("th",class_="d_ich")]
    print("Processed {} rows!".format(len(user_rows)))
    for row in user_rows:
        username = row.find("th",class_="d_ich").get_text()

        checked_inputs = []
        tds = row.find_all("td", class_="d_gc")
        for td in tds:
            check = td.find("input", checked="checked")
            if check:
                checked_inputs.append(reg_enrollment.search(check['title']).group(1))

        if len(checked_inputs) > 1:
            problematic_users.append((username,"enrolled in too many groups: {}".format(checked_inputs)))

        for group in checked_inputs:
            if group in group_list:
                group_list[group][1].append(username)
            else:
                print("This should never happen")

        if not checked_inputs:
            ungrouped_users.append(username)

print()
count = 0
for ta,val in group_list.items():
    ta_name = reg_custom.match(ta).group(1)
    print(val[0], len(val[1]), "\t", ta_name)
    count = count + len(val[1])
    ta_short = ta_name.split(" ")[0].lower()
    with open("./group_{}".format(ta_short),"w") as f:
        for name in val[1]:
            f.write(name + "\n")

with open("./nogroup","w") as f:
    for name in ungrouped_users:
        f.write(name + "\n")

count = count + len(ungrouped_users)
print(count)
print(problematic_users)


