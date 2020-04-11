# Codi font en Python 

## Per executar el programa:

``` python.exe habitaclia_scraper.py ```

Fa scraping de pisos en lloguer en Les comarques del Barcelonès i adjacents

Veure comentaris al codi "habitaclia_scraper.py" per utilitzar el scraper en diferents modalitats

## Descripció dels fitxers:

- **habitaclia_scraper.py:** Punt d'entrada de l'aplicació. Instancia el scraper i el crida indicant llistes de URLs als indexos 
d'oferta o URL directes a ofertes
- **Habitaclia.py:** Classe de python que fa la feina del scraping
- **http_helper.py:** Encapsula les requests a les webs de habitaclia incloent un senzill mecanisme d'espaiat en les peticions
- **log_helper.py:** Petita capa de la llibreria logging de Python. Permet "loguejar" els possibles errors en un fitxer, 
així com la sortida del detall del procés en el canal stdout   

