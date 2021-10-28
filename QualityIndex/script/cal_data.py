#!/usr/bin/python3
import os
import csv
import yaml
from datetime import datetime, timedelta

### get config
project_root = '/var/www/html/QualityIndex'
config = project_root+'/data/config'
raw_data_file = project_root + '/data/raw_data.csv'

try:
    stream = open(config, 'r')
except:
    print("============================")
    print("!! open config file error !!")
    print("----------------------------")
    raise

try:
    conf = yaml.safe_load(stream)
    LPBP = int(conf['LPBP'])
    psi_begin = conf['Current PSI Begin']
    psi_end = conf['Current PSI End']
except:
    print("===============================")
    print("!! config file content error !!")
    print("-------------------------------")
    raise

try:
    stream.close()
except:
    pass



def cal_result(raw_data):
    line = {}
    ### calculate Z
    begin_date = datetime.strptime(psi_begin,"%Y.%m.%d")
    end_date = datetime.strptime(psi_end,"%Y.%m.%d")
    data_date = datetime.strptime(raw_data['date'][:8], "%Y%m%d")

    past_days = (data_date - begin_date).days + 1
    check_date = begin_date
    workdays = 0
    for i in range(past_days):
        weekday = check_date.strftime("%a")
        if weekday != "Sun" and weekday != "Sat":
            workdays += 1
        check_date += timedelta(days=1)
    #print(past_days)
    #print(workdays)
    Z = workdays

    x_b = int(raw_data['x_block'])
    x_c = int(raw_data['x_critical'])
    x_s = int(raw_data['x_serious'])
    x_m = int(raw_data['x_medium'])
    y_b = int(raw_data['y_block'])
    y_c = int(raw_data['y_critical'])
    y_s = int(raw_data['y_serious'])
    y_m = int(raw_data['y_medium'])


    
    
    ### function X
    X = ((x_b+x_c)/(3*3)+x_s/(3*10)+x_m/(3*50))*100
    
    ### calculate Y
    Y = y_b* 11.1 + y_c* 11.1 + y_s* 3.33 + y_m* 0.666

    ### debug
    #print(X)
    #print(Y)
    #print(LPBP)
    #print(Z)
    
    ### calculate Accumulated Index
    #Accumulated_Index = X/2+(Y/(LPBP*0.85))*50
    Accumulated_Index = X/2+(Y/LPBP)*50 # new equation 20191106
    
    ### calculate Index_with_which_day

    #Index_with_which_day = X/2+((Y/(LPBP*0.85))/(Z/(5*9)))*50
    Index_with_which_day = X/2+((Y/LPBP)/(Z/(5*9)))*50 # new equation 20191106

    line['date'] = datetime.strptime(raw_data['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    line['X'] = round(X,2)
    line['Y'] = round(Y,2)
    line['Z'] = Z
    line['LPBP'] = LPBP 
    line['Accumulated_Index'] = round(Accumulated_Index,2)
    line['Index_with_which_day'] = round(Index_with_which_day,2)

    return line


### get raw_data
post_rows = []
with open (raw_data_file, 'r') as rf:
    for row in csv.DictReader(rf):
        print(row)
        post_row = cal_result(row)
        post_rows.append(post_row)
post_rows = reversed(post_rows)


result = project_root + '/data/result.csv'
with open(result, 'w') as csvfile:
    fieldnames = ['date', 'X', 'Y','Z', 'LPBP', 'Accumulated_Index', 'Index_with_which_day']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(post_rows)



