from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.files import File
from STReport.models import ST_log
from STReport.forms import *
from datetime import datetime
from time import mktime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from DFT.settings import MEDIA_ROOT
import logging
from collections import defaultdict
import sys
import re
import time
import csv
import pdb
import os

logger = logging.getLogger('log')


class ReportDetail(DetailView):
    model = ST_log


class ReportList(ListView):
    model = ST_log


def list_reports(request):
    d_pk_list = []
    d_title_list = []

    ### delete the selected reports
    if (request.POST.get('action') == 'delete'):
        all_pk_list = list(map(lambda x: x.pk, ST_log.objects.all()))
        d_pk_list = list(filter(lambda x: request.POST.get(str(x)) == 'on', all_pk_list))
        d_title_list = list(map(lambda x: ST_log.objects.get(pk=x).title, d_pk_list))
        confirm_delete = request.POST.get('confirm_delete')
        request.session['d_pk'] = d_pk_list
        data = {
            'd_pk_list': d_pk_list,
            'd_title_list': d_title_list,
        }
        response = TemplateResponse(request, 'STReport/confirm_delete.html', data, )
        return response

    ### confirm the action before delete
    elif (request.POST.get('action') == 'confirm_delete'):
        d_pk_list = request.session['d_pk']
        for pk in d_pk_list:
            ST_log.objects.filter(id=pk).delete()

    list_form = ST_log_list_Form(request.POST)
    reports = ST_log.objects.all().order_by('-begin_time')
    data = {
        'list_form': list_form,
        'reports': reports,
        'd_pk_list': d_pk_list,
        'd_title_list': d_title_list,
    }

    response = TemplateResponse(request, 'STReport/list_reports.html', data, )
    return response


def add_anno(request):
    e_pk = request.POST.get('e_pk')
    process_names = request.POST.get('title')
    # object=get_object_or_404(ST_log, id=e_pk)
    object = ST_log.objects.get(pk=e_pk)
    typecsv = {}
    csvform = CSV_chart_Form()
    rowcsv = []
    list = []
    new_rows = []
    fieldnames = []
    csvform = CSV_chart_Form(request.POST)
    if (request.POST.get('action') == 'submit'):
        if csvform.is_valid():
            with open(MEDIA_ROOT + 'streport/' + process_names + '.csv', 'r', encoding='utf-8') as csvfile:
                if csvfile:
                    reader = csv.DictReader(csvfile)

                    #    rowcsv.remove("Time Passed")
                    for row in reader:
                        if (csvform.data['timecol'] == row["Time Passed"]):
                            row['Anno Name ' + csvform.data['selection']] = csvform.data['anno_name']
                            row['Anno Text ' + csvform.data['selection']] = csvform.data['anno_text']
                            typecsv = row
                        new_rows.append(row)
                    rowcsv = reader.fieldnames
                    for string in rowcsv:
                        if not (string.find("Time") or string.find("Anno")):
                            list.append(string)

                    fieldnames = reader.fieldnames
            csvfile.close()
            # write a new csv file
            with open(MEDIA_ROOT + 'streport/' + process_names + '.csv', 'w', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
                writer.writeheader()
                for row in new_rows:
                    writer.writerow(row)
            csvfile.close()
    data = {
        'object': object,
        'typecsv': typecsv,
        'row': list,
        'csvform': csvform
    }

    response = TemplateResponse(request, 'STReport/add_anno.html', data, )
    return response


def edit_report(request):
    form_err = ''
    e_pk = request.POST.get('e_pk')
    report = get_object_or_404(ST_log, id=e_pk)
    form = ST_log_Form(request.POST or None, instance=report)
    if (request.POST.get('action') == 'save'):
        if form.is_valid():
            form.save()
            data = {
                'object': report,
            }
            response = TemplateResponse(request, 'STReport/st_log_detail.html', data, )
            return response

        else:
            form_err = form.errors

    data = {
        'form': form,
        'object': report,
        'form_err': form_err,
    }

    response = TemplateResponse(request, 'STReport/edit_report.html', data, )
    return response


def edit(request):
    data = {
    }
    response = TemplateResponse(request, 'stest/edit_report.html', data, )
    return response


def list_report(request):
    data = {
    }
    response = TemplateResponse(request, 'stest/report_list.html', data, )
    return response


def index(request):
    #    cate_form = PE_Category.objects.all()
    data = {
        #        'cate_form': cate_form,
    }

    response = TemplateResponse(request, 'pages/index.html', data, )
    return response


def get_recommend_process(memory_file):
    start_flag_pat = re.compile(b'\s+PID\s*SZ\s*RSZ')
    end_flag_pat = re.compile(b'^\s+$')
    data_pat = re.compile(b'^\s*(\d+)\s+\d+\s+(\d+)\s+\d+\s+\S+\s+\S+\s+(.+)$')
    results = defaultdict(list)
    data_flag = False
    pid_des = {}

    for line in memory_file:
        search_end_flag = end_flag_pat.search(line)
        logging.info("==============search_end_flag={}=============".format(search_end_flag))
        if search_end_flag:
            data_flag = False

        if data_flag == True:
            search_data = data_pat.search(line)
            pid = search_data.group(1).decode('utf8')
            rsz = search_data.group(2).decode('utf8')
            des = search_data.group(3).decode('utf8')
            if pid not in pid_des.keys():
                pid_des[pid] = des
            results[pid].append(rsz)

        # data flag
        search_start_flag = start_flag_pat.search(line)
        if search_start_flag:
            data_flag = True
    new_results = []
    for x, y in results.items():
        if len(y) <= 6:
            continue  # ignore process which existance short than 1 hour
        else:
            y = y[6:]  # ignore data in the 1st hour
        y = [int(yy) for yy in y]
        max_i = max(y)
        min_i = min(y)
        if min_i != 0:
            mag = round(max_i / min_i, 2)
            diff = max_i - min_i
            new_results.append([x, mag, diff, max_i, min_i])

    sorted_results = sorted(new_results, key=lambda l: l[2], reverse=True)
    # The pid with the largest gap between the first two RSZ is obtained
    recommend_pid = [x[0] for x in sorted_results[:2]]
    recommend_des = [pid_des[x] for x in recommend_pid]
    logger.info("recommend_pid=={}".format(recommend_pid))
    logger.info("len(recommend_des)======{}".format(len(recommend_des)))
    return recommend_des


def import_log(request):
    #    pdb.set_trace()
    #    pdb.run('print ao.as_atble()', locals())

    form_err = ''
    dt_str_list = []
    file_name = ''
    csv_path = ''
    csv_name = ''
    p_name_list = []
    new_plot_pk = -1
    d_title = ''
    begin_time = ''
    begin_time_str = ''
    end_time_str = ''
    process_names = ''
    fn_nopost = ''
    workstation_name = ''
    workstation_model = ''
    device = ''
    tcct_tape = ''
    st_tape = ''

    if request.POST.get('action') == 'import':

        #        start = time.clock()
        count = 0
        iformatt = ''

        iform = ST_log_import_Form(request.POST, request.FILES)
        process_names = request.POST.get('process_names')
        choose_VSZ = request.POST.get('choose_VSZ')
        choose_RSZ = request.POST.get('choose_RSZ')
        logger.info('process_names:{}, choose_VSZ:{}, choose_RSZ:{}'.format(process_names, choose_VSZ, choose_RSZ))
        # get recommend process name and combine with focus process name set in the import log web page
        f = request.FILES['data_log']
        # allFiles = request.FILES
        logger.info('=======f:{}=========='.format(f))
        # logger.info('=======allFiles:{}=========='.format(allFiles))
        p_name_list_recommend = get_recommend_process(f)
        p_name_list_focus = re.split(',', process_names)
        # filter process not already in p_name_list
        # p_name_list_recommend = [ x for x in p_name_list_recommend if not any( y in x for y in p_name_list_focus ) ]
        p_name_list = p_name_list_recommend + p_name_list_focus
        logger.info("=====p_name_list======={}===".format(p_name_list))
        # get name before postfix
        file_name = request.FILES.get('data_log')
        pat_fn_nopost = re.compile("(.+)\.txt", re.I)
        search_fn_nopost = pat_fn_nopost.search(str(file_name))
        if search_fn_nopost:
            fn_nopost = search_fn_nopost.group(1)
            csv_name = fn_nopost + '.csv'
            csv_path = './files/stest/' + csv_name
        else:
            csv_path = ''
            fn_nopost = 'NONE'

        tu_dic = {}
        su_dic = {}
        tu_flag = 0
        su_flag = 0
        process_flag = {}
        # time
        dt_str = ''
        time_diff = {}
        hd_dict_data = defaultdict(dict)

        # regex 4 basic information
        pat_wn = re.compile(b"workstation name:\s*(.+)\n", )
        pat_wm = re.compile(b"workstation model:\s*(.+)\n", )
        pat_dv = re.compile(b"device:\s*(.+)\n", )
        pat_tt = re.compile(b"testcell tape:\s*(.+)\n", )
        pat_st = re.compile(b"smartest tape:\s*(.+)\n", )

        pat_tu = re.compile(b"^\s*Total:\s+\d+\s+(\d+)", )  # regex 4 Total used memory
        pat_su = re.compile(b"^\s*Swap:\s+\d+\s+(\d+)", )  # regex 4 Swap used memory
        # pat_datetime = re.compile(b"^\s*SNAPSHOT:\s*(.+)$", )  # regex 4 get time
        pat_datetime = re.compile(b"^\s*SNAPSHOT:\s*(.+)$", )  # regex 4 get time
        pat_cst = re.compile("CST", )  # regex 4 change time zone name CST to China Standart Time

        pat_hd = re.compile(b"Hard Disk Space", )

        # regex 4 all process
        p_pat_list = {}
        p_rsz_dict_data = {}
        p_vsz_dict_data = {}
        for p_name in p_name_list:
            p_pat_list[p_name] = re.compile(b"^\s*\d+\s+\d+\s+(\d+)\s+(\d+).+" + bytearray(p_name, 'utf-8'), re.I)
            process_flag[p_name] = 0
            p_rsz_dict_data[p_name] = {}
            p_vsz_dict_data[p_name] = {}
        # process data log file
        f = request.FILES['data_log']

        sct1 = 0
        sct2 = 0
        sct3 = 0
        fl_count = 0
        data_count = 0
        hd_flag = 3  # hd_flag = 2 will get hard disk data
        # data processing
        for line in f:
            fl_count += 1
            # search HardDisk data
            hd_flag += 1
            search_hd = pat_hd.search(line)
            if search_hd:
                hd_flag = 0
            # get Hard Disk Space
            if hd_flag == 2:
                hd_used = line.split()[0]
                hd_avail = line.split()[1]
                hd_dict_data['Used'][dt_str] = round(int(hd_used) / 1024 / 1024 / 1024, 4)
                hd_dict_data['Avail'][dt_str] = round(int(hd_avail) / 1024 / 1024 / 1024, 4)

            # search basic information in the top x(=fl_count) lines
            if fl_count <= 10:
                search_wn = pat_wn.search(line)
                search_wm = pat_wm.search(line)
                search_dv = pat_dv.search(line)
                search_tt = pat_tt.search(line)
                search_st = pat_st.search(line)
                if search_wn:
                    workstation_name = search_wn.group(1)
                if search_wm:
                    workstation_model = search_wm.group(1)
                if search_dv:
                    device = search_dv.group(1)
                if search_tt:
                    tcct_tape = search_tt.group(1)
                if search_st:
                    st_tape = search_st.group(1)
            # get current p_name RSZ VSZ
            for p_name in p_name_list:
                if process_flag[p_name] == 1:
                    search_process = p_pat_list[p_name].search(line)
                    if search_process:
                        if choose_RSZ:
                            p_rsz_dict_data[p_name][dt_str] = round(
                                int(search_process.group(1).decode("utf-8")) / 1024 / 1024, 4)
                        if choose_VSZ:
                            p_vsz_dict_data[p_name][dt_str] = round(
                                int(search_process.group(2).decode("utf-8")) / 1024 / 1024, 4)
                        process_flag[p_name] = 0
            # get total
            if tu_flag == 1:
                search_tu = pat_tu.search(line)
                if search_tu:
                    tu_dic[dt_str] = round(int(search_tu.group(1).decode("utf-8")) / 1024 / 1024, 4)  # unit is GB
                    tu_flag = 0
            # get swap
            if su_flag == 1:
                search_su = pat_su.search(line)
                if search_su:
                    su_dic[dt_str] = round(int(search_su.group(1).decode("utf-8")) / 1024 / 1024, 4)
                    su_flag = 0
            # get snapshot time, the current time is every half minute
            search_datetime = pat_datetime.search(line)
            if search_datetime:
                data_count += 1
                time_string = search_datetime.group(1).decode("utf-8").strip("\r")
                # time_string = pat_cst.sub("China Standard Time", time_string)
                dt_struct = time.strptime(time_string, "%a %b %d %X %Z %Y")
                dt_time = datetime.fromtimestamp(mktime(dt_struct))
                dt_str = time.strftime("%Y-%m-%d %H:%M", dt_struct)
                dt_str_list.append(dt_str)

                tu_flag = 1
                su_flag = 1
                for p_name in p_name_list:
                    if choose_VSZ:
                        p_vsz_dict_data[p_name][dt_str] = ''
                    if choose_RSZ:
                        p_rsz_dict_data[p_name][dt_str] = ''
                    if process_flag[p_name] == 0:
                        process_flag[p_name] = 1

                # get begin time
                if (data_count == 1):
                    # begin_time = dt_str
                    begin_time = dt_time
                    begin_time_str = dt_str

                # get end time
                end_time_str = dt_str

                # calculate time passed
                time_diff[dt_str] = int((dt_time - begin_time).seconds) // 360 / 10 + (dt_time - begin_time).days * 24

                # elapsed = (time.clock() - start)

        # Write all data into csv file with empty annotation.
        with open(MEDIA_ROOT + 'streport/tmp.csv', 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['Time Passed', 'Total Used', 'Anno Name Total Used', 'Anno Text Total Used', 'Swap Used',
                          'Anno Name Swap Used', 'Anno Text Swap Used']

            # add set process to field name
            for p in p_name_list:
                if choose_VSZ:
                    fieldnames.append(p + ' vsz')
                    fieldnames.append('Anno Name ' + p + ' vsz')
                    fieldnames.append('Anno Text ' + p + ' vsz')
                if choose_RSZ:
                    fieldnames.append(p + ' rsz')
                    fieldnames.append('Anno Name ' + p + ' rsz')
                    fieldnames.append('Anno Text ' + p + ' rsz')

            # for HardDisk data
            if (hd_dict_data):
                fieldnames.append('HardDisk Used')
                fieldnames.append('HardDisk Avail')
            # tooltip try
            # fieldnames.append('tooltip')
            # write header to csv file
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            logger.info("===dt_str_list=={}".format(dt_str_list))
            logger.info("hd_dict_data===={}".format(hd_dict_data))
            if dt_str_list:
                for dt in dt_str_list:
                    row_dic = {
                        # 'Date Time':dt,
                        'Time Passed': time_diff[dt],
                        'Total Used': tu_dic[dt],
                        'Anno Name Total Used': '',
                        'Anno Text Total Used': '',
                        'Swap Used': su_dic[dt],
                        'Anno Name Swap Used': '',
                        'Anno Text Swap Used': '',
                    }
                    for p in p_name_list:
                        if choose_VSZ:
                            row_dic[p + ' vsz'] = p_vsz_dict_data[p][dt]
                        if choose_RSZ:
                            row_dic[p + ' rsz'] = p_rsz_dict_data[p][dt]
                    if (hd_dict_data):
                        row_dic['HardDisk Used'] = hd_dict_data['Used'][dt]
                        row_dic['HardDisk Avail'] = hd_dict_data['Avail'][dt]
                    ### tooltip try
                    # row_dic['tooltip']='try'
                    writer.writerow(row_dic)

        # get data automatically
        tf = open(MEDIA_ROOT + 'streport/tmp.csv', encoding='utf-8')
        sf = File(tf)
        sf.name = csv_name
        d_title = fn_nopost

        iform.data = iform.data.copy()
        iform.files["data_csv"] = sf
        iform.data["title"] = d_title
        iform.data['begin_time'] = begin_time_str
        iform.data['end_time'] = end_time_str
        iform.data['workstation_model'] = workstation_model
        iform.data['workstation_name'] = workstation_name
        iform.data['device'] = device
        iform.data['st_tape'] = st_tape
        iform.data['tcct_tape'] = tcct_tape

        # Save after validateion or return err
        if iform.is_valid():
            new_plot_data = iform.save()
            new_plot_pk = new_plot_data.pk
        else:
            # me=request.FILES.get('data_log')
            form_err = iform.errors
            new_plot_pk = -2

        tf.close()
        sf.close()

        debug_data = new_plot_pk
        debug_data2 = sct2
        debug_data3 = sct3
        ###############################################
        ##############  Edited by #####################
        ############## Jiayu Zhu  #####################
        ##############  Begin    ######################
        ###############################################
        # Process other file
        i = 1
        searchname = 'attach' + str(i)
        while searchname in request.FILES:
            iformatt = ST_log_attach_Form(request.POST, request.FILES)
            otherf = request.FILES[searchname]
            iformatt.data['log_pk'] = new_plot_pk
            iformatt.files['attachment'] = otherf
            i = i + 1
            searchname = 'attach' + str(i)
            if iformatt.is_valid():
                iformatt.save()
            else:
                iformatt_err = iformatt.errors


    else:
        iform = ST_log_import_Form()
        ######also edited by Jiayu Zhu #####
        iformatt = ST_log_attach_Form()

    ###############################################
    ##############  Edited by #####################
    ############## Jiayu Zhu  #####################
    ##############    End    ######################
    ###############################################
    #    form = ST_log_Form()

    ### Save to the database
    if (request.POST.get('action') == 'save'):
        new_plot_pk = request.POST.get('pk')
        if new_plot_pk:
            log_instance = get_object_or_404(ST_log, id=new_plot_pk)
            iform = ST_log_import_Form(request.POST or None, instance=log_instance)
            # form['data_log']=file_name
            #            setattr(form,'data_log',file_name)
            if iform.is_valid():
                iform.save()
            else:
                form_err = iform.errors
        else:
            form_err = iform.errors
    data = {
        'iform': iform,
        'form_err': form_err,
        'd_title': d_title,
        'begin_time': begin_time_str,
        'end_time': end_time_str,
        'workstation_model': workstation_model,
        'workstation_name': workstation_name,
        'device': device,
        'st_tape': st_tape,
        'tcct_tape': tcct_tape,
        'csv_path': csv_path,
        'new_plot_pk': new_plot_pk,
        'process_names': process_names,
        #            'duration_data':duration_data,
        ##### Edit by Jiayu Zhu ########
        'iformatt': iformatt,
        ##### Edit by Jiayu Zhu ########
    }

    response = TemplateResponse(request, 'stest/import_log.html', data, )
    return response
