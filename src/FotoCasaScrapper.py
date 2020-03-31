import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import re

class FotoCasaScrapper():

    def __init__(self,webdriver_path=None, init_url = r'https://www.fotocasa.es/es/comprar/terrenos/alcover/todas-las-zonas/l?latitude=41.264&longitude=1.1699&combinedLocationIds=724,9,43,268,0,43005,0,0,0'):
        self.driver = webdriver.Chrome(webdriver_path)
        self.driver.implicitly_wait(10)
        
        self.regex_size = '^([\d\.,]+)\s*m²$'
        self.regex_price = '^([\d\.,]+)\s*€$'
        self.re_size = re.compile(self.regex_size)
        self.re_price = re.compile(self.regex_price)
        self.static_fast_pause_time = 2
        self.random_fast_pause_time = 3
        self.static_pause_time = 10
        self.random_pause_time = 10

        self.driver.get(init_url)

    def GetListOfHouses(self, base_url = r'https://www.fotocasa.es/es/comprar/viviendas/barcelona-capital/todas-las-zonas/l?latitude=41.3854&longitude=2.1775&combinedLocationIds=724,9,8,232,376,8019,0,0,0'):
        rList = None

        self.driver.get(base_url)
        time.sleep(self.random_pause_time * random.random() + self.static_pause_time)

        self.GetToBottomOfPage()
        
        rList = pd.concat([self.SingleCardInfo(card) for card in self.driver.find_elements_by_class_name("re-Card")])
        if self.HasNextPage():
            time.sleep(self.random_pause_time * random.random() + self.static_pause_time)
            rList = pd.concat([rList, self.GetListOfHouses(self.GetNextPage())])

        return(rList)        

    def HasNextPage(self):
        return (not (self.driver.find_element_by_xpath("//*[text()='>']") == None))

    def GetNextPage(self):
        return (self.driver.find_element_by_xpath("//*[text()='>']").get_attribute("href"))

    def GetToBottomOfPage(self, number_of_pag_downs = 17):
        for i in range(number_of_pag_downs + random.randint(0, 4)):
            time.sleep(self.random_fast_pause_time * random.random() + self.static_fast_pause_time)
            try:
                self.driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            except:
                self.driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
    
    def SingleCardInfo(self, card):
        rCardInfo = None

        if('ad-ClickTracker' not in card.get_attribute("class")):

            link = card.find_elements_by_class_name("re-Card-link")[0].get_attribute("href")
            
            title = card.find_elements_by_class_name("re-Card-title")[0].text
            
            size = None
            if(card.find_elements_by_class_name("re-Card-feature")):
                for element in card.find_elements_by_class_name("re-Card-feature"):
                    if (self.re_size.match(element.text)):
                        size = int(re.sub(self.regex_size, '\\1', element.text, 0, re.MULTILINE))
            
            price = None            
            if(card.find_elements_by_class_name("re-Card-price")[0].text):
                for element in card.find_elements_by_class_name("re-Card-price"):
                    if (self.re_price.match(element.text)):
                        price = int(re.sub(self.regex_price, '\\1', element.text, 0, re.MULTILINE).replace('.',''))

            rCardInfo = pd.DataFrame({'Link': link, 'Title': title, 'Size': size, 'Price': price}, index=[0])

        return(rCardInfo)
