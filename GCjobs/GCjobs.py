'''
Created on Mar 27, 2010
This module is designed to populate the jobs database for sourceforge.net.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] GoogleCodeJobs.py [datasource_id] [Test T/F]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'.

@author: StevenNorris
'''

import sys
from GCutils import GoogleCodeUtils
import traceback
import socket

#adds the jobs to the sf_jobs table in the selected database
def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print ("""RUN INSTRUCTIONS\n
        Run this module from command line with the following format:\n
        [Interpreter] GoogleCodeJobs.py [datasource_id] [Test T/F]\n
        Test is a string variable. Be sure to use a capital 'T' to denote test mode.\n 
        Otherwise use 'F'.""")
        sys.exit()
    
    #checks for test mode
    if(test=='T'):
        try:
            print("TEST MODE ACTIVATED")
            utils=GoogleCodeUtils()
        except:
            print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
            sys.exit()
    else:
        try:
            utils=GoogleCodeUtils('dbInfo.txt')
        except:
            print("Please create the dbInfo.txt and the dbInfoText.txt files. See ReadMe for formatting.")
            sys.exit()   
        
    #gathering project unixnames
    try:
        print("Gathering unixnames.")
        projects_list=utils.get_projects(datasource_id)
        print(len(projects_list))
        
        #checks test mode for project amount to be collected
        if(test=='T'):
            end=50
        else:
            end=len(projects_list)
        
        #adds jobs to database
        try:
            print("Creating Jobs")
            for project in projects_list:
                project=project[0]
                print("Creating job for "+project)
                try:
                    insert='''INSERT INTO gc_jobs (unixname,datasource_id,status,last_modified,modified_by)
                    VALUES(%s,%s,'gather_home',NOW(),%s)'''
                    utils.db_insert(insert,project,datasource_id,socket.gethostname())
                except:
                    print('!!!!WARNING!!!! Job creation failed for '+project+'.')
                    print(traceback.format_exc())
        except:
            print('!!!!WARNING!!!! Jobs did not create succesfully')
            print(traceback.format_exc())
    except:
        print('!!!!WARNING!!!! Projects unixnames not collected properly.')
        print(traceback.format_exc())
    
def test(argv):
    utils=GoogleCodeUtils('dbInfoTest.txt') 

main(sys.argv)
          


