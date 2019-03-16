# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 20:06:16 2019

@author: malte
"""

import group_functions

import pickle
import os


cwd = os.getcwd()

def resobject(file):
    with open(file, "rb") as pfile:
        resinfo = pickle.load(pfile)
        return resinfo

def create_text(res_obj):

    months = len(res_obj.unprocessed_month)
    
    text = "This resolution is concerning " + str(months) + " months \n"
    
    for idx, month in enumerate(res_obj.unprocessed_month):
        text += "Statistics for " + month[:-4] + " [mmyy]: \n"
#
        text += "Outlays of this month:\n"
        for outl in res_obj.personal_stats_read[idx]:
            name = group_functions.name_by_id(outl[0])
            outlay = outl[2]
            nominal = outl[1]
            diff = outl[3]
            text += name + " paid " + str(outlay) + " with a balance at " + str(nominal) + " therefore a difference of " + str(diff) + "\n"

    text += "\n"
    text += "Statistics for the whole resolution intervall:\n"
    
    for item in res_obj.personal_stats_sum:
        name = group_functions.name_by_id(item[0])
        outlay = item[2]
        nominal = item[1]
        diff = item [3]
        text += name + " paid " + str(outlay) + " with a balance at " + str(nominal) + " therefore a difference of " + str(diff) + "\n"
    
    text += "\n"    
    text += "Transactions calculated by the script for the whole resolution intervall: \n"
    
    for item in res_obj.transaction_list:
        debtorname = group_functions.name_by_id(item[1])
        creditorname = group_functions.name_by_id(item[0])
        amount = item[2]
        
        text += debtorname + " has to pay " + str(amount) + " to " + creditorname + "\n"
        
    return text