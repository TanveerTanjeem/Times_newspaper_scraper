from selenium import webdriver
import bs4 as bs
import time
import re
import requests
#from selenium.webdriver.common import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import ui 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv



url = "https://www.lancashiretelegraph.co.uk/search/?search=social%20distance&sort=relevance&headline_only=false&site_id[]=66&posted_date=custom&posted_date_from=13-Mar-2020&posted_date_to=14-Jun-2020&pp=20&p=0"
word_bank = ["coronavirus","Coronavirus","\"coronavirus","\"Coronavirus","Covid-19","covid-19","social distance","Social Distance","lockdown","Lockdown","wear mask","Wear Mask","stay indoors","Stay Indoors","quarantine","Quarantine","pandemic","Pandemic","social distancing","Social Distancing"]
driver = webdriver.Firefox()
driver.get(url)

#overcome cookie popup

try:
    press_accept = driver.find_element_by_id("I Accept")
    if press_accept!='':
        press_accept.send_keys(Keys.ENTER)
        
except TimeoutException:
    pass


#enter keywords to get relevant articles
inputElement = driver.find_element_by_class_name("search-bar")
inputElement.find_element_by_tag_name("input").clear()
inputElement.find_element_by_tag_name("input").send_keys('coronavirus social distance lockdown wear mask stay indoors quarantine pandemic social distancing', Keys.ENTER)
time.sleep(6)
driver.find_element_by_class_name("custom-select-container").find_element_by_xpath("//select/option[text()='oldest']").click()
time.sleep(4)

#list all articles
articles = driver.find_elements_by_class_name("article")
i=0

with open('blackburn.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Occurence"])


 
#open Articles one by one
for article in articles:
    found=0
    date = article.find_element_by_class_name("article-date").text
    driver2 = webdriver.Firefox()
    driver2.get(article.get_attribute('href'))  
    
    #overcome cookie message
    try:
        press_accept = driver2.find_element_by_id("I Accept")
        if press_accept!='':
            press_accept.send_keys(Keys.ENTER)
        
    except TimeoutException:
    
        pass
    
    
    if press_accept!='':
        press_accept.send_keys(Keys.ENTER)
    
    time.sleep(2)
    title =""
    text=""
    try:
        title = driver2.find_element_by_class_name("headline").text
    except NoSuchElementException: 
        pass
            
    
    

    for word in word_bank:
        if re.search(word,title):
            print("found",word,"in",title),    
            with open('blackburn.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([date,"1"])   
            found=1
            break
            

    if found==1:
        driver2.close()            
    else:
        try:
            text = driver2.find_element_by_id("article").text
        except NoSuchElementException:
            pass  

        
        for word in word_bank:
             
            if re.search(word,text):
                print("found",word,"in para",text) 
                with open('blackburn.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([date,"1"])   
                break

        driver2.close()    
    

    i+=1
    if i==30:
        break
    
driver.close()