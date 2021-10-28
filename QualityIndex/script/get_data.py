#!./bin/python3
from jira import JIRA
import re
import os
import csv
import yaml
from datetime import datetime


### get config
project_root = '/var/www/html/QualityIndex'
config = project_root+'/data/config'

try:
    stream = open(config, 'r')
except:
    print("============================")
    print("!! open config file error !!")
    print("----------------------------")
    raise

try:
    conf = yaml.safe_load(stream)
    jql_x = conf['jql_x']
    jql_y = conf['jql_y']
except:
    print("===============================")
    print("!! config file content error !!")
    print("-------------------------------")
    raise

try:
    stream.close()
except:
    pass


### start query
options = {
        'server': 'https://wetrack.advantest.com/'}
jira_user = 'sha_stats.script.user'
jira_password = 'X8YR*DeM9CqmAwNt'

jira = JIRA(options=options, basic_auth=(jira_user, jira_password))

y_query = jira.search_issues(jql_y, maxResults=500)

#print(len(y_query))

y_b_count = 0
y_c_count = 0
y_s_count = 0
y_m_count = 0

for q in y_query:
    priority = str(q.fields.priority)

    if priority == 'Blocker':
        y_b_count += 1
    elif priority == 'Critical':
        y_c_count += 1
    elif priority == 'Serious':
        y_s_count += 1
    elif priority == 'Medium':
        y_m_count += 1

x_query = jira.search_issues(jql_str=jql_x, maxResults=500)
x_b_count = 0
x_c_count = 0
x_s_count = 0
x_m_count = 0

for q in x_query:
    priority = str(q.fields.priority)
    if priority == 'Blocker':
        x_b_count += 1
    elif priority == 'Critical':
        x_c_count += 1
    elif priority == 'Serious':
        x_s_count += 1
    elif priority == 'Medium':
        x_m_count += 1

query_date = datetime.now().strftime("%Y%m%d%H%M%S")

data = {
    'date'      : query_date,
    'x_block'   : x_b_count,
    'x_critical': x_c_count,
    'x_serious' : x_s_count,
    'x_medium'  : x_m_count,
    'y_block'   : y_b_count,
    'y_critical': y_c_count,
    'y_serious' : y_s_count,
    'y_medium'  : y_m_count
}

print(data)

raw_data = project_root + '/data/raw_data.csv'
if not os.path.exists(raw_data):
    with open (raw_data, 'w') as csvfile:
        fieldnames = ['date', 'x_block', 'x_critical', 'x_serious', 'x_medium', 'y_block', 'y_critical', 'y_serious', 'y_medium']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

with open(raw_data, 'a') as csvfile:
    fieldnames = ['date', 'x_block', 'x_critical', 'x_serious', 'x_medium', 'y_block', 'y_critical', 'y_serious', 'y_medium']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(data)

'''

### calculate
print(X)
print(Y)


### wirte data to file

data_file = project_root+'/data/data.csv'
if not os.path.exists(data_file):
    with open(data_file,'w') as csvfile:
        fieldnames = ['date','Accumulated_Index','Index_with_which_day','x', 'y', 'ldp', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

with open(data_file,'w') as csvfile:
    writer = csv.DictWriter(csvfile)
    writer.writerow(data_dict)





'''
