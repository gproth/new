'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project downloads pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com/p/"

import sys
import time
import traceback

def run(utils,datasource_id):
    print("\nGathering downloads pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_downloads")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("Gathering for "+unixname)
            
            #gets home page
            downloads=utils.get_page(BASE_LINK+unixname+"/downloads/list")
            
            #inserts home page
            if(downloads):
                insert="""UPDATE gc_project_indexes SET downloadshtml=%s, last_modified=NOW() WHERE unixname=%s AND datasource_id=%s"""
                utils.db_insert(insert,downloads,unixname,datasource_id)
                utils.change_status('gather_issues','gather_downloads',datasource_id,unixname)
                
                #get new job
                job=utils.get_job(datasource_id,'gather_downloads')
                if(utils.error):
                    sys.exit()
            
            #if downloads page does not collect properly, post error and get new job
            else:
                print("!!!!WARNING!!!! Downloads page gathering failed for "+unixname)
                utils.post_error('gather_downloads: \nDownloads page either did not exist or fail to collect.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_downloads')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! Downloads page collection failed")
            utils.post_error('gather_downloads:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_downloads')
            if(utils.error):
                sys.exit()
