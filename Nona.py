from bs4 import BeautifulSoup as bs
import requests , shutil, os
from termcolor import colored, cprint 
mainurl = "https://hanascan.com/"
appstatus = True
oriDir = os.getcwd()
headers = {
    'authority': 'jack.mhscdnv4.club',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
   }
def downloader(url):
    
    r = requests.get(url)
    c = r.content
    soup = bs(c,"html.parser")
    
    chapnum = url.split(".")[-2].split("-")[-1]
    if chapnum in os.listdir():
        print("This Chapter Already exists")
        

    else:
        os.mkdir(chapnum)
        os.chdir(os.getcwd()+"/"+chapnum)
        images = soup.find_all("img",{"class":"chapter-img"})
        x = 1
        for image in images:
            cprint(images.index(image)+1,"magenta")
            imgurl = image["data-original"]
            ext = imgurl.split(".")[-1]
        
            pagename = str(x) + "." + ext
            print(pagename)
            r = requests.get(imgurl, stream = True , headers=headers)
            # Check if the image was retrieved successfully
            r.raw.decode_content = True
            with open(pagename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            x+=1       
        

while appstatus == True:

    cprint("---------------------------------------------" , "magenta")    
    cprint("----------  Nona Raw Down By Yuhan  ----------","white","on_red")
    cprint("---------------------------------------------" , "magenta")
    cprint("Enter a manga name ","white")
    cprint("------------------","magenta")
    search = input()
    sl = "https://hanascan.com/manga-list.html?name=" + search
    r = requests.get(sl)
    c = r.content
    soup = bs(c,"html.parser")
    mcontainer = soup.find_all("div",{"class":"media"})
    if len(mcontainer) < 1:
        cprint("Zannen . No Manga with same name Found !!","red")
        cprint("Try another one","white")
        pass
    else :
        n1 = True
        while n1==True:
            
            cprint("---------------------------------------------" , "magenta")
            for i in mcontainer :
                link = i.find("a")["href"]
                linklen = len(link)
                dash = "-"*int(linklen/2)
                
                name = i.find("h3",{"class":"media-heading"}).find("a").text
                cprint(str(mcontainer.index(i)+1)+ " - " +name,"magenta")
                # namear = i.find_all("a")[2].text
                
                cprint("---------------------------------------------" , "magenta")
                # cprint(link,"white")
            cprint("0 - Back to main menu")
            cprint("---------------------------------------------" , "magenta")
            cprint("Yuupi , Select one Onegaishimassu","green")    
            cprint("Choose a number ..  ","green")  
            selected = int(input())-1
            if selected == -1:
                n1=False
            else:
                n2 = True
                while n2 == True:
                    os.chdir(oriDir)
                    ml = mainurl + mcontainer[selected].find("a")["href"]
                    mn = mcontainer[selected].find("h3",{"class":"media-heading"}).find("a").text.replace(":","")
                    nc = requests.get(ml).content
                    nsoup = bs(nc,"html.parser")
                    chaptersbox = nsoup.find("div",{"class":"list-wrap"})
                    chapters = chaptersbox.find_all("p")
                    chapters.reverse()
                    latest = int(chapters[len(chapters)-1].find("span",{"class":"title"}).find("a")["title"].split(" ")[-1])
                    gap =  latest - len(chapters) 
                    cprint(str(len(chapters)) + " Chapters found... " + "From  " + str(gap) + " to " + str(latest),"white")
                    cprint("Last Chapter is  .. " + str(latest) ,"green")
                    cprint("1 Download all   2 Download by chapter  3 Download by range  4 Back","magenta")
                    dwchoice = int(input())
                    if dwchoice == 4:
                        n2 = False
                    elif  dwchoice == 1:
                        if mn in os.listdir():
                            pass
                        else:
                            os.mkdir(mn)
                        x=1
                        for chapter in chapters :
                            
                            os.chdir(oriDir+"/"+mn)
                            cl = mainurl + chapter.find("span",{"class":"title"}).find("a")["href"]
                            try:
                                downloader(cl)
                                cprint("Reminder : To force stop press Ctrl+C twice","red")
                            except:
                                pass
                            cprint(str(x)+" Chapters Downloaded")
                            x+=1
                        cprint("Done !! , Want another manga ?","white") 
                        cprint("1 - YES, Please","green")   
                        cprint("2 - No , Just Close","red")
                        n1 = False
                        n2 = False
                        if int(input()) == 1:
                            pass
                        elif int(input()) == 2:
                            cprint("GoodBye !! Have a good day","cyan")
                            appstatus = False

                    elif dwchoice == 2 :
                        
                        if mn in os.listdir():
                            pass
                        else:
                            os.mkdir(mn)
                        os.chdir(oriDir+"/"+mn)
                        cprint("Choose one chapter","green" )
                        choosenchap = int(input()) - gap
                        cl = mainurl + chapters[choosenchap-1].find("span",{"class":"title"}).find("a")["href"]
                        downloader(cl)  
                        cprint("One Chapter Downloaded")
                        cprint("Done !! , Want another manga ?","white") 
                        cprint("1 - YES, Please","green")   
                        cprint("2 - No , Just Close","red")
                        n1 = False
                        n2 = False
                        if int(input()) == 1:
                            pass
                        elif int(input()) == 2:
                            cprint("GoodBye !! Have a good day","cyan")
                            appstatus = False
                    elif dwchoice == 3 :
                        if mn in os.listdir():
                            pass
                        else:
                            os.mkdir(mn)
                        cprint("choose first chapter","green")
                        Rfrom = int(input())
                        cprint("choose last chapter","green")
                        Rto = int(input())
                        x=1
                        for i in range (Rfrom, Rto+1):
                            os.chdir(oriDir+"/"+mn)
                            cl = mainurl + chapters[i-1].find("span",{"class":"title"}).find("a")["href"]
                            try:
                                downloader(cl)
                            except:
                                pass
                            cprint(str(x)+" Chapters Downloaded")    
                            x+=1
                        cprint("Done !! , Want another manga ?","white") 
                        cprint("1 - YES, Please","green")   
                        cprint("2 Twice- No , Just Close","red")
                        n1 = False
                        n2 = False
                        finish = input()
                        if int(finish) == 1:
                            pass
                        elif int(finish) == 2:
                            cprint("GoodBye !! Have a good day","cyan")
                            appstatus = False        