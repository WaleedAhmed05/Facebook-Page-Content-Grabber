from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib
import re
import os

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('log-level=3')
options.add_argument("--disable-notifications")



driver = webdriver.Chrome('chromedriver.exe', options=options)
Page_link="https://www.facebook.com/penduproductions"

driver.get(Page_link)


content=requests.get(Page_link).text
soup=BeautifulSoup(content,'lxml')




def _extract_image(item):
    postPictures = item.find_all(class_="scaledImageFitWidth img")
    image = ""
    for postPicture in postPictures:
        image = postPicture.get('src')
    return image


def Download_ChromeDriver():
    import zipfile
    downlink='https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_win32.zip'#Latest chromedriver download link for windows
    print("Downloading...")
    urllib.request.urlretrieve(downlink, "webdriver.zip")
    with zipfile.ZipFile("webdriver.zip", 'r') as zip_pos:
        print("Unzipping...")
        zip_pos.extractall()
    os.remove("webdriver.zip") 




def DownloadPhotos(post_link,n):
    
    print("In Download Photos Method")
    #print(post_link)
    post_link=post_link.replace("www.", "m.", 1)
    
    driver.execute_script("window.open('"+post_link+"');")
    driver.switch_to.window(driver.window_handles[-1])
    
    
#    print(post_link)
    
    elems = driver.find_elements_by_xpath("//a[@href]")
    
   # n=1
    for elem in elems:
        if ".jpg" in elem.get_attribute("href"):
            
            post_link=elem.get_attribute("href")
            #print(post_link)
            
            page_source = driver.page_source
            
            
            regex_name=r'<title[^>]*>([^<]+)</title>'
            photoname=re.findall(regex_name, page_source)[0]
            photoname=photoname.translate({ord(i): None for i in '|*\/:?<>'})
            
            if not os.path.exists("Downloaded_Pictures"):
                os.makedirs("Downloaded_Pictures")
            
            try:
                if not os.path.exists("Downloaded_Pictures/"+str(photoname)+'.jpg'):
                    urllib.request.urlretrieve(post_link, "Downloaded_Pictures/"+str(photoname)+'.jpg')
                else:
                    urllib.request.urlretrieve(post_link, "Downloaded_Pictures/"+str(photoname)+str(n)+'.jpg')
                print("Photo Downloaded")
            except:
                print("Invalid Characters in pictures name. ")
                print("Saving picture as: "+"Photo_"+str(n))
                urllib.request.urlretrieve(post_link, "Downloaded_Pictures/"+'photo'+str(n)+'.jpg')
                print("Photo Downloaded")
        #    n=n+1
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
     
    
    



def Likes_counter(post_link):
    
    driver.execute_script("window.open('"+post_link+"');")
    driver.switch_to.window(driver.window_handles[-1])    
    driver.close()
    driver.switch_to.window(driver.window_handles[0]) 

    
    


if not os.path.exists("chromedriver.exe"):
    print("Chromedriver doesn't exist, Downloading Webdriver...")
    Download_ChromeDriver() 


elems = driver.find_elements_by_xpath("//a[@href]")
print(elems)
n=1
for elem in elems:
    
    if "photos/pb" in elem.get_attribute("href"):
        
        print("Post no: "+str(n))
        post_link=elem.get_attribute("href")
        print(post_link)
        post=requests.get(str(post_link)).text
        
        soup2=BeautifulSoup(post,'lxml')
        post_title=soup2.title.string
        print(post_title)
        Likes_counter(post_link)
        DownloadPhotos(post_link,n)
        print("-----------------------")
        n=n+1
