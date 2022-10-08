from html import entities
import requests
import json
import csv

GROUPS = []
USERSBYGROUP = []

x = requests.get("{{INSERT URL HERE}/rest/api/2/applicationrole}", headers={"Content-Type":"application/json","Authorization":"Basic {INSERT AUTH TOKEN HERE}"})

y = x.json()

for t in y:
    GROUPS.append(t['groups'])

#Print All Groups in Jira System
#Modify index in GROUPS[0] from [0] to [1] to print Jira Software License Users
#print(json.dumps(GROUPS[0], indent = 2))

for group in GROUPS[0]:
    USERS = []
    x = requests.get(f"{INSERT URL HERE}/rest/api/2/group/member?groupname={group}", headers={"Content-Type":"application/json","Authorization":"Basic {INSERT AUTH TOKEN HERE}"}).json()
    if len(x['values']) > 0:
        for i in x['values']:
            USERS.append(i['name'])        
    USERSBYGROUP.append({'groupname': group, 'totalusers': len(x['values']), 'users': USERS})

print(json.dumps(USERSBYGROUP, indent = 2))

with open('jira-agent-licenses.json', 'w', encoding='utf-8') as f:
    json.dump(USERSBYGROUP, f, ensure_ascii=False, indent=4)
    
jsondata = USERSBYGROUP
 
data_file = open('jira-agent-licenses.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
 
data_file.close()