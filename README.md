# Home Scraper 
## UOC - Tipologia i cicle de vida de les dades
Alumnes:
- Marc Serra Suñol
- Javier Beltran Lou

## Descripció dels fitxers
- A la carpeta [./src](./src) hi ha el codi font de la solució. Veure la wiki de la carpeta per una descripció dels fitxers font.
- A la carpeta [./pdf](./pdf) hi ha el fitxer [Respostes.pdf](./pdf/Respostes.pdf) amb les respostes a les preguntes.
 
## Web Scraper de sites amb informació sobre lloguers d'habitatges
## Context
La idea d'aquest Web Scraper és la d'obtenir un Dataset d'informació sobre lloguers d'habitatges a la zona de Barcelona i rodalies, tot i que es pot fer 
servir per obtenir també vivendes a la venda de qualsevol regió (població, comarca, província) contemplada en el website target

El website "scrapejat" és https://www.habitaclia.com/ . Els motius per triar aquest website van ser:
1. Conté informació abundant sobre lloguers d'habitatges
2. La dificultat de fer scraping es va considerar mitja i menor en comparició amb altre sites que també es van intentar, concretament https://www.fotocasa.es/, 
la qual és una altra marca del mateix grup

## Títol
Habitatges en règim de lloguer a l'àrea de Barcelona

## Descripció del Dataset
Llistat d’habitatges en règim de lloguer als municipis de l’àrea de Barcelona (Barcelona i rodalies) 
per poder fer estudis comparatius segons diferents criteris

## Camps del CSV

- Id: Identificador de l'habitatge 
- URL: URL de la oferta obtinguda
- Tipus Oferta: Indica si es tracta d'un habitatge en Venda o en Lloguer. En el nostre CSV trobem només 'lloguer', el qual és el objectiu inicial del scraper.
- Tipus immoble: Pis, Casa, Àtic o Dúplex
- Municipi: per exemple, 'Barcelona'
- Província: pe exemple, 'Barcelona'
- Zona: Barri o zona dins d'un municipi on es situa l'habitatge. Per exemple, 'Dreta de l'Eixample'
- Preu: Preu, en euros, de l'habitatge en el moment d'obtenir les dades
- Data: Data en què es va obtenir la informació de l'habitatge
- Superfície: Superfície, en metres quadrats, de l'habitatge
- \#Habitacions: Nombre d'habitacions de què consta l'habitatge
- \#Banys: Nombre de banys de què consta la vivenda
- Antiguitat: Any de construcció de la vivenda 
- Planta: Número de planta (1ª, 2ª, ...)
- Parking: booleà indicant si la vivenda disposa o no de pàrking
- Calefacció: booleà indicant si la vivenda disposa o no de calefacció
- Aire acondicionat: booleà indicant si la vivenda disposa o no de aire acondicionat
- Moblat: booleà indicant si la vivenda disposa o no de mobles
- Ascensor: booleà indicant si la vivenda disposa o no d'ascensor
- Jardí: booleà indicant si la vivenda disposa o no de jardí
- Eficiència energètica: Classificació de la vivenda segons la seva eficiència energètica (A..G),
- Classe emissions: Classificació de la vivenda segons les  emissions (A..G)

Cal tenir en compte que no tots els habitatges disposen de tots els camps d'informació. Per aquells camps dels quals no es disposa d'alguna 
dada el valor reportat és un valor buit o ''.