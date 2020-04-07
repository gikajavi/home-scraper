from Habitaclia import HabitacliaScraper

scraper = HabitacliaScraper()
scraper.start()
# scraper.scrap_index_page("https://www.habitaclia.com/alquiler-barcelona-2.htm")
# scraper.scrap_data_page("https://www.habitaclia.com/alquiler-piso-cerca_de_la_playa_barceloneta-barcelona-i26933003769842.htm?st=1,4,9,11,13&coddists=100&codzonas=103&f=&from=list&lo=55")
# scraper.scrap_data_page("https://www.habitaclia.com/alquiler-piso-via_augusta_349_355_via_augusta_349_355_sarria-barcelona-i672001759190.htm?f=&geo=p&from=list&lo=55")
# https://www.habitaclia.com/alquiler-piso-barceloneta_barceloneta-barcelona-i4190003644357.htm?f=&geo=p&from=list&lo=55

scraper.write_to_csv('dataset.csv')
