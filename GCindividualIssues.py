'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project individual issue pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com"

import sys
import time
import traceback
import re

#This method spiders the given page for the individual issue links
def issuesSpider(html):
    links=[]
    matches=re.findall('<a href="(detail\?id=.+?)"',html)
    if (len(matches)!=0):
        for match in matches:
            id=match[10:]
            links.append((id,match))
        return links
    else:
        return None
    
#This method spiders the given page for the next page link
def nextSpider(html):
    matches=re.search('<a href="(?P<Link>list\?start=.+?)">Next',html)
    if (matches):
        return matches.group('Link')
    else:
        return None

def run(utils,datasource_id):
    print("\nGathering individual issues pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_issues_specific")
    if(utils.error):
        sys.exit()
    while(job!=None):
        try:
            unixname=job[0]
            print ("Gathering for "+unixname)
            
            #gets issues page
            issues=utils.get_issues(datasource_id, unixname)
            if(issues):
                issues=issues[0]
            else:
                issues=None
            ids=utils.get_issue_ids(unixname)
            page_num=1
            
            #starts page searching for every page of issues
            next=True;
            error=False;
            while(next):
                print("\tGathering for page "+str(page_num))
                
                #checks issue page for None-type and forbidden page
                if(issues):
                    if(re.search('<title>Project hosting on Google Code</title>',issues)==None):
                        
                        #Gathers and inserts pages for each issue
                        links=issuesSpider(issues)
                        if(links):
                            for link in links:
                                id=int(link[0])
                                link=link[1]
                                if(not id in ids):
                                    time.sleep(3)
                                    print("\t\tInserting issue id "+str(id)+" for "+unixname)
                                    issuePage=utils.get_page(BASE_LINK+"/p/"+unixname+"/issues/"+link)
                                    insert="""INSERT IGNORE INTO gc_issues_indexes (unixname,issue_id,html,datasource_id,last_modified)
                                    VALUES(%s,%s,%s,%s,NOW())"""
                                    utils.db_insert(insert,unixname,id,issuePage,datasource_id)
                                else:
                                    print"\t\tIssue id "+str(id)+" has already been collected for "+unixname
                            
                            #checks for next page and collects accordingly
                            next_link=nextSpider(issues);
                            if(next_link):
                                page_num=page_num+1
                                issues=utils.get_page(BASE_LINK+"/p/"+unixname+"/issues/"+next_link)
                            else:
                                next=False
                        
                        #If no links are found, halt loop
                        else:
                            print("\t!! No links found for "+unixname+" at page "+str(page_num))
                            next=False
                    
                    #If home page is forbidden, halt loop
                    else:
                        print("\t!! Home page led to a forbidden page.")
                        next=False
                        
                #if home page gathering fails, set error and halt loop
                else:
                    print("!!!WARNING!!!! Issues page gathering failed for "+unixname+" page "+page_num)
                    error_msg='gather_issues_specific: \nIssues page did not collect correctly.'
                    error=True
                    next=False
            
            #if error set, post error and get new job
            if(error):
                utils.post_error(error_msg,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_issues_specific')
                if(utils.error):
                    sys.exit()
                
            #change status and get new job
            else:
                utils.change_status("completed","gather_issues_specific",datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_issues_specific')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! Individual issue pages collection failed")
            utils.post_error('gather_issues_specific:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_issues_specific')
            if(utils.error):
                sys.exit()    

