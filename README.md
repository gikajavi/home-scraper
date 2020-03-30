# Home Scraper 
## UOC - Tipologia i cicle de vida de les dades
Alumnes:
- Marc Serra Suñol
- Javier Beltran Lou

En aquesta primera versió presentem una primera idea per tal de de ser avaluada en el "pre lliurament" de la pràctica. Veure secció "Dubtes / Dificultats"
d'aquest fitxer.

**Alternatives (per si aquesta proposta es considera arriscada):**
- Scraper d'ofertes de cotxes de segona mà (coches.net)
- Vademecum espanyol https://www.vademecum.es/
- Scraper de webs esportives (marca.com, sport.es) 

Aparentment, les webs anteriors no presenten les dificultats trobades a la proposta present

## Web Scraper de sites amb informació sobre lloguers d'habitatges
## Context
La idea d'aquest Web Scraper és la d'obtenir un Dataset d'informació sobre lloguers d'habitatges a la zona de Barcelona i rodalies.

Inicialment es plantejarà el scraping d'alguna de les webs més populars al respecte (Fotocasa, habitaclia, Idealista). 
Aquests llocs web representen un percentatge molt gran del mercat de lloguer a Barcelona. De fet, 
l'scraping parcial de qualsevol d'aquests sites ja pot permetre la generació d'un Dataset amb prou informació 
per fer estudis interessants sobre el mercat del lloguer en el context de Barcelona i rodalies.

## Títol
Habitatges en règim de lloguer a l'àrea de Barcelona

## Descripció del Dataset
Llistat d’habitatges en règim de lloguer als municipis de l’àrea de Barcelona (Barcelona i rodalies) 
per poder fer estudis comparatius segons diferents criteris

## Representació gràfica
TODO

## Camps

- Municipi: El municipi / població on està localitzat el habitatge
- Barri: Barri o districte (per ciutats grans com Barcelona).
- PreuActual: El preu mensual en euros del lloguer
- Tipus: Enumeració: Pis / Casa / ¿altres?
- Metres: Metres quadrats de l’habitatge
- Antiguitat: Antiguitat de l’immoble
- NombreHabitacions: Quantitat d’habitacions de l’immoble
- NombreBanys: Quantitat de banys de l’immoble
- Planta: Número de planta de l’immoble (1ª, 2ª, ...)
- Ascensor: Si l’edifici disposa o no d’ascensor
- Parking: Enumeració: No disposa / individual / Comunitari / ¿altres?
- Moblat: Booleà per indicar si l’immoble està o no moblat
- Jardi: Booleà per indicar si l’immoble te jardi o no

Aquesta llista és provisoinal. Algns camps poden no aparèixer a la versió final, i potser s'inclouran d'altres. En particular, s'està considerant
d'afegir un identificador de l'habitatge, un camp PreuInicial i dates de creació / modificació que podrien aportar informació interessant de cara 
a un anàlisi evolotiu de preus més acurat.

## Agraïments
TODO

## Inspiració / possibles aplicacions
1. Estudi de diferències de preu / m2 entre municipis (barris, districtes, zones, carrers). Tamnbé antiguitat, etc, ...
2. Evolució preu / m2 (en el context de vàries extraccions en diferents moments) classificant per municipi, antiguitat, etc
3. Increment mig de preu en els habitatges que disposen de parking i/o altres criteris
4. (...)

## Dubtes / Dificultats
Hem trobat que les webs objectiu, després d'unra primera inspecció, presenten impediments a nivell de robots.txt. Unes primeres proves a nivell de codi
ens han fet veure que son "scrapejables" però amb algunes dificultats (cal, per exemple, dependre d'intereracció manual per superar alguna prova CAPTCHA)





 


