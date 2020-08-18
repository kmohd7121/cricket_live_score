"""
We are Scraping Cricket sports score from famous website Cricbuzz,
and then analyzing them using the Pandas library.
"""
"""
The components of a web page
When we visit a web page, our web browser makes a request to a web
server. This request is called a GET request, since we're getting files
from the server. The server then sends back files that tell our browser
how to render the page for us. The files fall into a few main types:

HTML — contain the main content of the page.
CSS — add styling to make the page look nicer.
JS — Javascript files add interactivity to web pages.
Images — image formats, such as JPG and PNG allow web pages to show pictures.
After our browser receives all the files, it renders the page and displays it
to us. There's a lot that happens behind the scenes to render a page nicely,
but we don't need to worry about most of it when we're web scraping.
When we perform web scraping, we're interested in the main content of the web
page, so we look at the HTML.
"""
"""  ======================= Import libraries   ================== """
####   request library to import page content                ####
import requests

####  pandas library to analyze sports score data           ####
import pandas as p

####  bs4 library to extract data from different classes   ####
from bs4 import BeautifulSoup

####  re library to get the data in correct form               ####
import re

"""   =========************************  CODE BLOCK  ***********************================="""
try:
    page=requests.get("https://www.cricbuzz.com/cricket-match/live-scores")
    soup=BeautifulSoup(page.content, 'html.parser')
    #print(soup)
    score_page=soup.find(class_=" cb-col-67 cb-col cb-left cb-schdl")               #   THIS CLASS IS FOR WHOLE SCORE PAGE      ****
    #print(score_page)
    page_blocks=score_page.find_all(class_="cb-col cb-col-100 cb-lv-main")    #   THIS CLASS IS FOR BLOCKS OF CONTENTS   ****
    #print(page_blocks)
    first=page_blocks[0]


    """ ===========**************************** CODE HERE IS FOR EXTRACTING ITEMS FROM ONE BLOCK ********************==============="""

    """ all the information we want is in first
        1 > Title  like  INDIA  TOUR OF ENGLAND  2018
        2 > Teams  like India vs England
        3 > Match  like 3rd odi
        4 > Score  like ENGLAND 260/2 (44.3 Ovs)  •  INDIA 256/8 (50.0 Ovs)
        5 > Ground  like at Leeds ,Headingley Cricket Ground.
        6 > Result like England won by 8 wickets
        7 > Progress like in test match India A trail by 243 runs 
    """

    """
    title_=first.find(class_="cb-lv-grn-strip text-bold cb-lv-scr-mtch-hdr")       #  THIS CLASS IS FOR TITLE OF BLOCKS            **** 
    if title_ is None:
        print(" In first block of score page TITLE is not available")
    else:
        print(title_.get_text())
        
    teams=first.find(class_="text-hvr-underline text-bold")                                #  THIS CLASS IS FOR TEAMS NAME                 ****
    #print(teams.get_text())
    
    match=first.find(class_="text-gray")                                                            #  THIS CLASS IS FOR MATCH TYPE                 ****
    #print(match.get_text())

    score=first.find(class_="cb-lv-scrs-col text-black")                                      #  THIS CLASS IS FOR SCORE BOARD               ****  
    if score is None :
        print("Match is not started")
    else:
        print(score.get_text())

    ground=first.select(".text-gray .text-gray")                                                  #  THIS CLASS IS FOR GROUND NAME             ****
    #print(ground[0].get_text())
    
    result=first.find(class_="cb-lv-scrs-col cb-text-complete")                           #  THIS CLASS IS FOR RESULT                          ****
    if result is None:
        print("Result is not obtained yet")
    else:
        print(result.get_text())
        
    live=first.find(class_="cb-lv-scrs-col cb-text-live")                                      #  THIS CLASS IS FOR PROGRESS OF MATCH     **** 
    if live is None:
        print("Match is not streaming live")
    else:
        print(live.get_text())

    """

    """   =================****************   FROM HERE CODE IS FOR EVERY BLOCK   *************************================"""


    """ APPLYING LOOPON LIST OF PAGE_BLOCKS TO EXTRAXT DATA FROM EVERY BLOCK  """
    
    title=0
    Title=[]
    Team_name=[]
    Match_no=[]
    Scores_temp=[]
    Scores=[]
    Result=[]
    Progress=[]
    for page_block in page_blocks:
         Title_=page_block.find(class_="cb-lv-grn-strip text-bold cb-lv-scr-mtch-hdr")
         if Title_ is None:
             Title.append(Title[title-1])
         else:
             Title.append(Title_.get_text())
         title+=1
         Team_=page_block.find(class_="text-hvr-underline text-bold").get_text()
         Team_name.append(Team_)
         Match_no_=page_block.find(class_='text-gray').get_text()
         filtered_Match_no=re.sub('\xa0','',Match_no_)
         Match_no.append(filtered_Match_no)
         Score_=page_block.find(class_="cb-lv-scrs-col text-black")
         if Score_ is None:Scores_temp.append("Match is not started")
         else:
             Scores_=Score_.get_text()
             Scores_temp.append(Scores_)
         Result_=page_block.find(class_="cb-lv-scrs-col cb-text-complete")
         if Result_ is None:Result.append("Result is not obtained yet")
         else:
             Result.append(Result_.get_text())
         Progress_=page_block.find(class_="cb-lv-scrs-col cb-text-live")
         if Progress_ is None:Progress.append("Match is not streaming live")
         else:
             Progress.append(Progress_.get_text())
    Ground_name_tags=score_page.select(".cb-col.cb-col-100.cb-lv-main .cb-mtch-lst.cb-col.cb-col-100.cb-tms-itm .cb-col-100.cb-col.cb-schdl .text-gray .text-gray")
    Ground_name=[Mn.get_text() for Mn in Ground_name_tags]
    for score in Scores_temp:
        s=re.sub('\xa0','',score)
        Scores.append(s)

    """ IF YOU WANT THE O/P OF ABOVE CODE REMOVE FROM BELOW STATEMENTS  """
    #print(Title,len(Title))
    #print("\n\n")
    #print(Team_name,len(Team_name))
    #print("\n\n")
    #print(Match_no,len(Match_no))
    #print("\n\n")
    #print(Ground_name,len(Ground_name))
    #print("\n\n")
    #print(Scores,len(Scores))
    #print("\n\n")
    #print(Result,len(Result))
    #print("\n\n")
    #print(Progress,len(Progress))

    """
    combine the data into a Pandas DataFrame and analyze it. A DataFrame is an
    object that can store tabular data, making data analysis easy. 
    """
    
    Sport_Score=p.DataFrame({
        "Title":Title,
        "Team Name":Team_name,
        "Match  No or Type":Match_no,
        "Ground Name":Ground_name,
        "Scores":Scores,
        "Results":Result,
        "Progress":Progress})
    
    #print(Sport_Score)

    
    """  =================************************  HERE ANALYSIS OF DATA IS NOT DONE  *************************====================="""

    #writer = p.ExcelWriter('Sport_Score_Report.xlsx', engine='xlsxwriter')
    #Sport_Score.to_excel(writer, sheet_name='Sport_Score')
    #writer.save()
    
    """ ==============*********************  LITTLE BIT ANALYSIS IS PERFORMED THROGH THIS CODE  **************====================="""

    Is_INDIA=Sport_Score["Team Name"].str.contains("India")
    Sport_Score["Is India"]=Is_INDIA

    writer = p.ExcelWriter('Sport_Score_Report.xlsx', engine='xlsxwriter')
    Sport_Score.to_excel(writer, sheet_name='Sport_Score')
    writer.save()
    print("Scraping is done ","\n\n","Excel workbook is created in same folder where Cricket Program is stored with name Sport_Score_Report")

    

    """  *************===============EXCEPTIONS THAT CAN OCCUR  ===================*******************************""" 
except ValueError :
    print("Something Went Wrong")
except NameError:
    print("Something Went Wrong")
except AttributeError:
    print("Something Went Wrong")
except PermissionError:
    print(" Current Sheet is already created")
except :
    print("Network connection is not proper")

""" ==================**********************  PROGRAM IS END HERE  *********************=========================="""    
