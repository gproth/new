
'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project home pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com/p/"

import sys
import time
import traceback

def run(utils,datasource_id):
    print("\nGathering home pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_home")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("Gathering for "+unixname)
            
            #gets home page
            home=utils.get_page(BASE_LINK+unixname)
            
            #inserts home page
            if(home):
                insert="""INSERT INTO gc_project_indexes (unixname,homehtml,last_modified,datasource_id)
                VALUES(%s,%s,NOW(),%s)"""
                utils.db_insert(insert,unixname,home,datasource_id)
                utils.change_status('gather_updates','gather_home',datasource_id,unixname)
                
                #get new job
                job=utils.get_job(datasource_id,'gather_home')
                if(utils.error):
                    sys.exit()
            
            #if home page does not collect properly, post error and get new job
            else:
                print("!!!!WARNING!!!! Home page gathering failed for "+unixname)
                utils.post_error('gather_home: \nHome page either did not exist or fail to collect.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_home')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! Home page collection failed")
            utils.post_error('gather_home:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_index')
            if(utils.error):
                sys.exit()
