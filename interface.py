############

#Imports

############

import datetime
import os
import pickle

import group_functions
import dialogs
import main_functions
import resolution_to_textfile

############

#Globals

############

working_groupname = ""
month_list = []
cwd = os.getcwd()
working_month = object

############

#Funktionen

############

def ask_for_new_month():
    global working_month
    global working_groupname
    global cwd
    global month_list

    new_bool = dialogs.get_yesno("New month data-set? [y/n] ")
    
    if new_bool == "y":
        
        new_month = dialogs.get_date()
        working_month = main_functions.month(int(new_month[1]), int(new_month[0]))
        print("Daily Costs: "+str(round(working_month.costs.daily,2)))
        save_yn= dialogs.get_yesno("Save calculated month for "+working_groupname+ "? [y/n] ")
        
        if save_yn == "y":
            
           year = str(working_month.year)
           month = str(working_month.month)
           if len(month) == 1:
               month = "0"+month
           if len(year) == 1:
               year = "0"+year
           save_filename = month+year+".mon"
           
           if os.path.isfile(os.path.join(cwd,working_groupname,save_filename)):
               
               print("There is already data for this month.")
               working_month = object
               return 0
           
           else:
               
               fobj = open(os.path.join(cwd,working_groupname,save_filename) ,"wb")
               pickle.dump([working_month , datetime.datetime.now()] , fobj)
               fobj.close()           
               month_list.append(save_filename)
               print("Data saved in "+ save_filename)
               
               cut_to_month = dialogs.get_yesno("another month? [y/n]")
               if cut_to_month == "y":
                   return ask_for_new_month()
               
               cut_to_res = dialogs.get_yesno("redirect to resolution? [y/n]")
               if cut_to_res == "y":
                   make_resolution()

        else:
            print("Data deleted")
            working_month = object
            return 0
        return 1
    else:
        return 0

def make_resolution():
    global working_groupname
    
    res = main_functions.resolution(working_groupname)
    if len(res.unprocessed_month)>0:
        file_name = res.unprocessed_month[0][:-4]+"to"+res.unprocessed_month[-1][:-4]+".res"
        with open(os.path.join(cwd,working_groupname,file_name), "wb") as pfile:
            pickle.dump(res,pfile)
        restext = resolution_to_textfile.create_text(resolution_to_textfile.resobject(os.path.join(cwd,working_groupname,file_name)))
        textfilename = file_name[:-3]+"txt"
        fobj = open(textfilename,"w")
        fobj.write(restext)
        fobj.close
        print("TXT-Version of resolution saved in " + textfilename)
        return True
    else:
        print("No data to process")
        return False

############

#Mainmenue

############

def show_main():
    global working_groupname
    global month_list
    
    print()
    while(True):
        
        option_list = ["Load Group" , "Create Group"]

        if working_groupname != "":
            option_list.append("Edit group")
            option_list.append("Add new month-statistics")
            option_list.append("Calculate new billing")
            option_list.append("Show statistics")
        option_list.append("Exit")
        menu = {}
    
        for idx,item in enumerate(option_list):
            menu[idx]=item
    
        options=menu.keys()
        #    options.sort()
        for entry in options: 
            print (entry, menu[entry])

        selection=dialogs.get_number("Please Select:") 
        try:
            menu[selection]
        except KeyError:
            print("input error")
            return True
        
        if menu[selection] == 'Load Group':
            
            loaded_groupnames = group_functions.find_groups()
            
            if len(loaded_groupnames)>0:
                working_groupname = group_functions.load_group_interaction(loaded_groupnames)
                month_list = group_functions.month_list
            else:
                print("No groups found")
            
        elif menu[selection] == 'Create Group':
            
            working_groupname = group_functions.create_group()
            
        elif menu[selection] == ("Edit group"): 

            group_functions.edit_group(working_groupname)
            
        elif menu[selection] == ("Add new month-statistics"):
            
            ask_for_new_month()
            
        elif menu[selection] == ("Calculate new billing"): 

            make_resolution()
            
        elif menu[selection] == ("Show statistics"): 
            print("####")
            print ("Should show statistics here")
            print("####")
        elif menu[selection] == "Exit":
            print("Script is ending")  
            return 0
  
        else: 
            print ("Input Error" )
            
        return menu[selection]

print("Resolution V_2_1")
print("########################################################################")
print("Things to be worked on:")
print("-it would make sense not to set a bool in *.mon if processed, but to move processed files to a 'resolution'-directory. for now its okay the way it is.")
print("-statistics function for group/months")
print("-extra payments should be implemented in resolution-function")
print("#########################################################################")
print()
print("BUG: first textfile is saved in wrong directory")
print("Resolution-Script starting")

do = True
while do:
    do = show_main()
    if do != 0:
        do = True
    else:
        do = False