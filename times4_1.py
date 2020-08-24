from selenium import webdriver
import bs4 as bs
import time
import re
import requests
#from selenium.webdriver.common import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import ui 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
from selenium.webdriver.common.by import By
import os
duration = 2  # seconds
freq = 440 

#The urls holding the articles are defined here
urls = ["https://www.thetimes.co.uk/html-sitemap/2020-03-3","https://www.thetimes.co.uk/html-sitemap/2020-03-4","https://www.thetimes.co.uk/html-sitemap/2020-04-1","https://www.thetimes.co.uk/html-sitemap/2020-04-2","https://www.thetimes.co.uk/html-sitemap/2020-04-3","https://www.thetimes.co.uk/html-sitemap/2020-04-4","https://www.thetimes.co.uk/html-sitemap/2020-05-1","https://www.thetimes.co.uk/html-sitemap/2020-05-2","https://www.thetimes.co.uk/html-sitemap/2020-05-3","https://www.thetimes.co.uk/html-sitemap/2020-05-4","https://www.thetimes.co.uk/html-sitemap/2020-06-1","https://www.thetimes.co.uk/html-sitemap/2020-06-2"

#for each url the scraper is run
for url in urls:
    #words to be searched in each article title is defined here
    word_bank = ["coronavirus","Coronavirus","\"coronavirus","\"Coronavirus","Covid-19","covid-19","social distance","Social Distance","lockdown","Lockdown","wear mask","Wear Mask","stay indoors","Stay Indoors","quarantine","Quarantine","pandemic","Pandemic","social distancing","Social Distancing"]
    #browser is opened in the background using a webdriver
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    #the driver fetches the url
    driver.get(url)
    time.sleep(3)

    #the driver presses the consent button
    try:
        driver.switch_to.frame(driver.find_element_by_id("sp_message_iframe_216133"))
        driver.find_element_by_xpath('//*[@title="I Agree"]').click()
        driver.switch_to.default_content()
    except (NoSuchElementException,TimeoutException):
    
        print("cant click in i agree")
        pass

    #fetches the elements containing the article titile
    tags = driver.find_elements_by_css_selector('li.Sitemap-link')

    with open('times4_1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Occurence"])

    #the tags variable is iterated to find the article titles that have words matching the words from the word_bank 
    i=0
    for item in tags:
        cant_click=0
        
        for word in word_bank:
            if re.search(word,item.text):
                    #when the word is found the driver opens another windows and opens the article
                if i>0: 
                    print("found",word,"in",item.text)
                    driver2 = webdriver.Firefox(options=options)
                    try:
                        driver2.get(item.find_element_by_tag_name('a').get_attribute('href'))    
                    except WebDriverException:
                        pass
                    time.sleep(3)

                    #click on the consent page
                    try:
                        iframe = WebDriverWait(driver2, 10).until(EC.presence_of_element_located((By.ID, "sp_message_iframe_216133")))
                        driver2.switch_to.frame(iframe)
                        driver2.switch_to.default_content()
                    except (NoSuchElementException,TimeoutException)   
                        cant_click=1

                    #method 1 to extract the datetime info     
                    try:
                        date = driver2.find_element_by_class_name('responsiveweb__DatePublicationContainer-tglil3-1')
                        date_cleaned = date.get_attribute('innerHTML').split('>')[1].split(',')[0] 
                    # method 2 to extract the info    
                    except (NoSuchElementException):
                        date = driver2.find_elements_by_class_name('css-901oao')
                        for j in date:
                            
                            if re.search("<time",j.get_attribute('innerHTML')):
                                date=j
                                date_cleaned = date.get_attribute('innerHTML').split('>')[1].split(',')[0]      

                    #if the page is unresponsive and exception is caught a "cant click" entry is made into the csv
                    if cant_click==1 and date_cleaned==None:
                        with open('times4_1.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow(["cant click","1"])
                    else:
                        with open('times4_1.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow([date_cleaned,"1"])
                    #when the date is extracted from the article the browser window is closed
                    driver2.close()
                        
                    break
                i+=1           
    #when all the articles are parsed on that page the window is closed and the next url is fetched    
    driver.close()

os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
