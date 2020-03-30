class FotoCasaScrapper():

    def __init__(self, init_url = r'https://www.fotocasa.es/es/comprar/terrenos/alcover/todas-las-zonas/l?latitude=41.264&longitude=1.1699&combinedLocationIds=724,9,43,268,0,43005,0,0,0'):
        self.driver = webdriver.Chrome(r'd:\Downloads\chromedriver_win32\chromedriver.exe')
        self.driver.get(init_url)
        
        self.regex_size = '^([\d\.,]+)\s*m²$'
        self.regex_price = '^([\d\.,]+)\s*€$'
        self.re_size = re.compile(self.regex_size)
        self.re_price = re.compile(self.regex_price)


    def GetListOfHouses(self, base_url = r'https://www.fotocasa.es/es/comprar/viviendas/barcelona-capital/todas-las-zonas/l?latitude=41.3854&longitude=2.1775&combinedLocationIds=724,9,8,232,376,8019,0,0,0', params = None):
        rList = None

        self.driver.get(base_url)
        while(self.driver.find_element_by_xpath('//body').get_attribute('class') == 'block-page'):
            time.sleep(pause_time * random.random())
        self.GetToBottomOfPage()
        
        rList = pd.concat([self.SingleCardInfo(card) for card in self.driver.find_elements_by_class_name("re-Card")])
        if self.HasNextPage():
            time.sleep(0.5 * random.random())
            rList = pd.concat([rList, self.GetListOfHouses(self.GetNextPage())])

        return(rList)        

    def HasNextPage(self):
        return (not (self.driver.find_element_by_xpath("//*[text()='>']") == None))

    def GetNextPage(self):
        return (self.driver.find_element_by_xpath("//*[text()='>']").get_attribute("href"))

    def GetToBottomOfPage(self, number_of_pag_downs = 17, pause_time = 0.5):
        for i in range(number_of_pag_downs + random.randint(0, 4)):
            time.sleep(pause_time * random.random())
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
