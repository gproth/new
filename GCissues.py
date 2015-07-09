
'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project issues pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com/p/"

import sys
import time
import traceback

def run(utils,datasource_id):
    print("\nGathering issues pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_issues")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("Gathering for "+unixname)
            
            #gets home page
            issues=utils.get_page(BASE_LINK+unixname+"/issues/list")
            
            #inserts home page
            if(issues):
                insert="""UPDATE gc_project_indexes SET issueshtml=%s, last_modified=NOW() WHERE unixname=%s AND datasource_id=%s"""
                utils.db_insert(insert,issues,unixname,datasource_id)
                utils.change_status('gather_wiki','gather_issues',datasource_id,unixname)
                
                #get new job
                job=utils.get_job(datasource_id,'gather_issues')
                if(utils.error):
                    sys.exit()
            
            #if issues page does not collect properly, post error and get new job
            else:
                print("!!!!WARNING!!!! Issues page gathering failed for "+unixname)
                utils.post_error('gather_issues: \nIssues page either did not exist or fail to collect.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_issues')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! Issues page collection failed")
            utils.post_error('gather_issues:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_issues')
            if(utils.error):
                sys.exit()
