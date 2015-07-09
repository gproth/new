'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project people pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com/p/"

import sys
import time
import traceback

def run(utils,datasource_id):
    print("\nGathering people pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_people")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("Gathering for "+unixname)
            
            #gets home page
            people=utils.get_page(BASE_LINK+unixname+"/people/list")
            
            #inserts home page
            if(people):
                insert="""UPDATE gc_project_indexes SET peoplehtml=%s, last_modified=NOW() WHERE unixname=%s AND datasource_id=%s"""
                utils.db_insert(insert,people,unixname,datasource_id)
                utils.change_status('gather_downloads','gather_people',datasource_id,unixname)
                
                #get new job
                job=utils.get_job(datasource_id,'gather_people')
                if(utils.error):
                    sys.exit()
            
            #if people page does not collect properly, post error and get new job
            else:
                print("!!!!WARNING!!!! People page gathering failed for "+unixname)
                utils.post_error('gather_people: \nPeople page either did not exist or fail to collect.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_people')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! People page collection failed")
            utils.post_error('gather_people:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_people')
            if(utils.error):
                sys.exit()
