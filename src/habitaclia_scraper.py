from Habitaclia import HabitacliaScraper

scraper = HabitacliaScraper()
# Scraping habitatges en lloguer d'una llista de indexos per regions (per exemple comarques)
# Lloguers Barcelonés i comarques adjacents (Maresme, Baix Llobregat i els dos Vallès)
# llista = ['https://www.habitaclia.com/alquiler-en-barcelones.htm',
#           'https://www.habitaclia.com/alquiler-en-valles_occidental.htm',
#           'https://www.habitaclia.com/alquiler-en-valles_oriental.htm',
#           'https://www.habitaclia.com/alquiler-en-baix_llobregat.htm',
#           'https://www.habitaclia.com/alquiler-en-maresme.htm']
# scraper.start(llista)

# Scraping de vivendes a la venda al Garraf
# llista = ['https://www.habitaclia.com/comprar-vivienda-en-garraf/provincia_barcelona/listainmuebles.htm']
# scraper.start(llista)

# Scraping de vivendes tant en venda com en lloguer a la comarca del Barcelonés
# llista = ['https://www.habitaclia.com/viviendas-en-barcelones.htm']
# scraper.start(llista)

# Exemples de scraping per URLs individuals
# Pàgines 1 i 3 de barcelona:
# scraper.scrap_index_page("https://www.habitaclia.com/alquiler-barcelona.htm")
# scraper.scrap_index_page("https://www.habitaclia.com/alquiler-barcelona-2.htm")
# Pàgina 1 de barcelona tant comprar com lloguer
scraper.scrap_index_page("https://www.habitaclia.com/viviendas-en-barcelones.htm")


# Exemples per ofertes individuals
#scraper.scrap_data_page("https://www.habitaclia.com/alquiler-piso-cerca_de_la_playa_barceloneta-barcelona-i26933003769842.htm?st=1,4,9,11,13&coddists=100&codzonas=103&f=&from=list&lo=55")
#scraper.scrap_data_page("https://www.habitaclia.com/alquiler-piso-via_augusta_349_355_via_augusta_349_355_sarria-barcelona-i672001759190.htm?f=&geo=p&from=list&lo=55")
#scraper.scrap_data_page("https://www.habitaclia.com/alquiler-piso-can_girona_terramar_vinyet_carrer_cellerot_calle_cellerot_9_terramar_vinyet-sitges-i500003426117.htm?pag=27&f=&geo=c&from=list&lo=55")



# Generar el CSV un cop s'hagi fet el scraping desitjat
scraper.write_to_csv('dataset.csv')
