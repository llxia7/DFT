from django.shortcuts import render
from django.template.response import TemplateResponse
from DFT.settings import BASE_DIR
import csv


def list_log(request):
    scores = []
    with open(BASE_DIR + '/QualityIndex/data/result.csv', 'r') as csvfile:
        # fieldnames = ['date,X,Y,Z,LPBP,Accumulated_Index,Index_with_which_day']
        # reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        reader = csv.DictReader(csvfile)
        for line in reader:
            scores.append(line)
    data = {
        'scores': scores
    }

    response = TemplateResponse(request, 'qi/list_log.html', data, )
    return response
