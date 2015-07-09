'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project updates pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com/p/"

import sys
import time
import traceback

def run(utils,datasource_id):
    print("\nGathering updates pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_updates")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("Gathering for "+unixname)
            
            #gets home page
            updates=utils.get_page(BASE_LINK+unixname+"/updates/list")
            
            #inserts home page
            if(updates):
                insert="""UPDATE gc_project_indexes SET updateshtml=%s, last_modified=NOW() WHERE unixname=%s AND datasource_id=%s"""
                utils.db_insert(insert,updates,unixname,datasource_id)
                utils.change_status('gather_people','gather_updates',datasource_id,unixname)
                
                #get new job
                job=utils.get_job(datasource_id,'gather_updates')
                if(utils.error):
                    sys.exit()
            
            #if updates page does not collect properly, post error and get new job
            else:
                print("!!!!WARNING!!!! Updates page gathering failed for "+unixname)
                utils.post_error('gather_Updates: \nUpdates page either did not exist or fail to collect.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_updates')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! Updates page collection failed")
            utils.post_error('gather_updates:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_updates')
            if(utils.error):
                sys.exit()
