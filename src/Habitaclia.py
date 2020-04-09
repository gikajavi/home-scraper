import pandas as pd
import random
import log_helper  # Capa de la llibreria logging
import http_helper  # Helper de requests HTTP per implementar espaiat de peticions (retards exponencials)
import datetime
from bs4 import BeautifulSoup

class HabitacliaScraper():
    def __init__(self):
        self._current_url = ""
        self._session_id = "sess-" + str(random.random())
        self._data = pd.DataFrame()
        self._logger = log_helper.LogHelper("./logs/log-" + self._session_id, 'scraper', True)
        self._http_client = http_helper.HttpHelper(self._logger, 5, 2)
        self._logger.info("Habitaclia Scraper Iniciado")

    def start(self, urls_index_list):
        for url_index in urls_index_list:
            self._start(url_index)

    def _start(self, url):
        self._current_url = url
        html_code = self._descargar_indice()
        self.total_index_pages = int(self._get_total_index_pages(html_code))
        i = 0
        while i < self.total_index_pages:
            url_to_scrap = self.get_url_to_scrap_by_index(i)
            self.scrap_index_page(url_to_scrap)
            i += 1

    def get_url_to_scrap_by_index(self, index):
        if index == 0:
            return self._current_url
        else:
            to_scrap = self._current_url
            return to_scrap.replace('.htm', "-" + str(index) + '.htm')

    def scrap_index_page(self, url):
        try:
            self._logger.info("Index scraping en " + url)
            html = self._descargar_url(url)
            parser = BeautifulSoup(html, 'html.parser')
            links = parser.select(".list-item-title a")
            for link in links:
                self.scrap_data_page(link['href'])

        except Exception as ex:
            self._logger.error("Error en el index scraping " + str(ex))

    def scrap_data_page(self, url):
        try:
            self._logger.info("Data scraping en " + url)

            # Algunes poques ofertes són de fotocasa i habitaclia ja indica que la major part de la info. està allí.
            # No ens interessen per manca de qualitat (dades insuficients)
            if self._fotocasa_id(url):
                self._logger.warning("URL descartada (falta de datos)")
                return

            html = self._descargar_url(url)
            parser = BeautifulSoup(html, 'html.parser')

            if self._inmueble_no_disponible(parser):
                self._logger.warning('El servidor indicó "inmueble no disponible". Se aborta la página')
                return

            # Se obtienen de la URL
            housing_id = self._get_housing_id_by_url(url)
            tipus_immoble = self._get_housing_type_by_url(url)
            tipus_oferta = self._get_offer_type_by_url(url)
            # Alguns links no són dels tipus suportats (lloguer i/o vivenda). Acostumen a ser promocions posades al final de la llista que apareixen com a ofertes "normalitzades" en altre punts
            if tipus_oferta.lower() != 'lloguer' and tipus_oferta.lower() != 'venda':
                self._logger.warning('El link en proceso no resultó ser compra o alquiler. Se aborta la página')
                return

            # Se obtienen de la sección "summary"
            municipi = self._get_municipio(parser)
            provincia = self._get_provincia(parser)
            zona = self._get_zona(parser)
            preuactual = self._get_precio(parser)
            datapreu = datetime.datetime.today().strftime('%d-%m-%Y')
            superficie = self._get_superficie(html, parser)
            habitaciones = self._get_habitaciones(html, parser)
            baños = self._get_baños(html, parser)

            # Se obtienen de "Características generales"
            antiguedad = self._get_antiguedad(parser)
            planta = self._get_planta(parser)
            parking = self._general_feature_exists("Plaza parking", parser)
            calefaccio = self._general_feature_exists("Calefacción", parser)
            aire_acondicionat = self._general_feature_exists("Aire acondicionado", parser)
            moblat = self._general_feature_exists("Sin amueblar", parser)
            # Etiquetat eficiència energètica i d'emissions
            eti_consum = self._get_eti_eficiencia(parser)
            eti_emissions = self._get_eti_emissions(parser)

            # Se obtienen de "Equipamiento comunitario"
            jardi = self._community_feature_exists("Jardín", parser)
            ascensor = self._community_feature_exists("Ascensor", parser)

            df_row = pd.DataFrame({'Id': housing_id,
                                 'Url': url,
                                 'Tipus Oferta': tipus_oferta,
                                 'Tipus Immoble': tipus_immoble,
                                 'Municipi': municipi,
                                 'Provincia': provincia,
                                 'Zona': zona,
                                 'Preu Actual (€)': preuactual,
                                 'Data': datapreu,
                                 'Superfície (m2)': superficie,
                                 '#Habitacions': habitaciones,
                                 '#Banys': baños,
                                 'Antiguitat': antiguedad,
                                 'Planta': planta,
                                 'Parking': parking,
                                 'Calefacció': calefaccio,
                                 'Aire acondicionat': aire_acondicionat,
                                 'Moblat': moblat,
                                 'Eficiència energètica': eti_consum,
                                 'Classe emissions': eti_emissions,
                                 'Jardi': jardi,
                                 'Ascensor': ascensor}, index = [0])
            self._data = self._data.append(df_row, ignore_index=True)
            
        except Exception as ex:
            self._logger.error("Error en el data scraping " + str(ex))

    def _inmueble_no_disponible(self, parser: BeautifulSoup):
        return len(parser.select('.imagen-no-disponible302')) > 0

    def _fotocasa_id(self, url: str):
        url = url.replace('https://www.habitaclia.com/', '')
        return url.lower().startswith('fa')

    def _get_eti_eficiencia(self, parser: BeautifulSoup):
        try:
            eles = parser.select('.detail-rating .rating-box')
            for ele in eles:
                s: str = ele.text
                if s.lower().strip().startswith('consumo'):
                    o: str = ele.select('.rating')[0].text
                    return o.strip()
            return None
        except Exception as ex:
            self._logger.error("Error obteniendo la etiqueta de eficiencia energética. Se devuelve None " + str(ex))
            return None

    def _get_eti_emissions(self, parser: BeautifulSoup):
        try:
            eles = parser.select('.detail-rating .rating-box')
            for ele in eles:
                s: str = ele.text
                if s.lower().strip().startswith('emisiones'):
                    o: str = ele.select('.rating')[0].text
                    return o.strip()
            return None
        except Exception as ex:
            self._logger.error("Error obteniendo la etiqueta de emisiones. Se devuelve None " + str(ex))
            return None

    def _get_antiguedad(self, parser: BeautifulSoup):
        try:
            ele = self._get_general_ele(parser)
            if not ele:
                return None
            items = ele.select('ul li')
            for item in items:
                s = str(item.text).lower().strip()
                if s.startswith('año construcción'):
                    planta = s.replace('año construcción', '').strip()
                    return planta
            return None
        except Exception as ex:
            self._logger.error("Error obteniendo la antigüedad. Se devuelve None " + str(ex))
            return None

    def _get_planta(self, parser: BeautifulSoup):
        try:
            ele = self._get_general_ele(parser)
            if not ele:
                return None
            items = ele.select('ul li')
            for item in items:
                s = str(item.text).lower().strip()
                if s.startswith('planta número'):
                    planta = s.replace('planta número', '').strip()
                    return planta
            return None
        except Exception as ex:
            self._logger.error("Error obteniendo la planta. Se devuelve None " + str(ex))
            return None

    def _general_feature_exists(self, feature: str, parser: BeautifulSoup):
        try:
            ele = self._get_general_ele(parser)
            if not ele:
                return False
            items = ele.select('ul li')
            for item in items:
                if str(item.text).lower().strip() == feature.lower():
                    return True
            return False
        except Exception as ex:
            self._logger.error("Error obteniendo la característica general " + feature + " Se considerará que no existe " + str(ex))
            return False

    def _community_feature_exists(self, feature: str, parser: BeautifulSoup):
        try:
            ele = self._get_community_ele(parser)
            if not ele:
                return False
            items = ele.select('ul li')
            for item in items:
                if str(item.text).lower().strip() == feature.lower():
                    return True
            return False
        except Exception as ex:
            self._logger.error("Error obteniendo la característica de comunidad " + feature +
                      " Se considerará que no existe " + str(ex))
            return False

    def _get_general_ele(self, parser: BeautifulSoup):
        general_ele = self._get_element_from_details_section('Características generales', parser)
        return general_ele

    def _get_community_ele(self, parser: BeautifulSoup):
        community_ele = self._get_element_from_details_section('Equipamiento comunitario', parser)
        return community_ele

    def _get_element_from_details_section(self, h3_title: str, parser: BeautifulSoup):
        eles = parser.select(".detail article")
        for ele in eles:
            h3 = ele.select('h3')
            if not h3:
                return False
            if len(h3) > 0 and str(h3[0].text).lower().strip() == h3_title.lower().strip():
                return ele
        return False

    def _get_housing_id_by_url(self, url: str):
        try:
            l = url.split('/')
            l2 = l[3].split('.htm')
            l3 = l2[0].split('-')
            id = l3[len(l3) - 1]
            return id
        except Exception as ex:
            self._logger.error("Error obteniendo el Id de la oferta " + str(ex) + " Se aborta el scraping de esta URL")
            raise

    def _get_offer_type_by_url(self, url):
        try:
            l = url.split('/')
            suff: str = str(l[3]).lower()
            if suff.startswith('alquiler-'):
                return 'Lloguer'
            if suff.startswith('comprar-'):
                return 'Venda'
            return 'altres'
        except Exception as ex:
            self._logger.error("Error obteniendo el tipo de oferta " + str(ex) + " Se aborta el scraping de esta URL")
            raise

    def _get_housing_type_by_url(self, url):
        try:
            l = url.split('/')
            suff: str = str(l[3]).lower()
            if suff.startswith('alquiler-piso') or suff.startswith('alquiler-apartamento') or suff.startswith('comprar-piso') or suff.startswith('comprar-apartamento'):
                return 'piso'
            if suff.startswith('alquiler-casa') or suff.startswith('comprar-casa'):
                return 'casa'
            if suff.startswith('alquiler-duplex') or suff.startswith('comprar-duplex'):
                return 'duplex'
            if suff.startswith('alquiler-atico') or suff.startswith('comprar-atico'):
                return 'atico'
            return 'otros'
        except Exception as ex:
            self._logger.error("Error obteniendo el tipo de inmueble " + str(ex) + " Se aborta el scraping de esta URL")
            raise

    def _get_municipio(self, parser: BeautifulSoup):
        try:
            s = ''
            ltags = parser.select('#js-nom-pob-busacador')
            if len(ltags) > 0:
                s = ltags[0].get('value')
            else:
                ltags = parser.select('#js-nom-pob-buscador')
                if len(ltags) > 0:
                    s = ltags[0].get('value')
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo el municipio. Se devuelve '' " + str(ex))
            return ''

    def _get_provincia(self, parser: BeautifulSoup):
        try:
            s = ''
            ltags = parser.select('#js-nom-prov-buscador')
            if len(ltags) > 0:
                s = ltags[0].get('value')
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo la provincia. Se devuelve None " + str(ex))
            return None

    def _get_zona(self, parser: BeautifulSoup):
        try:
            s = parser.select("article.location h4 a")[0].text.strip()
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo la zona por article.location. Se intenta con id_buscador " + str(ex))
            s = self._get_zona_by_buscador_input(parser)
            return s

    def _get_zona_by_buscador_input(self, parser: BeautifulSoup):
        try:
            s = ''
            ltags = parser.select('#js-nom-zona-buscador')
            if len(ltags) > 0:
                s = ltags[0].get('value')
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo la zona por id_buscador. Se devuelve None " + str(ex))
            return None

    def _get_precio(self, parser: BeautifulSoup):
        try:
            s = parser.select(".summary .price span[itemprop=price]")[0].text.strip()
            s = s.replace('€', '').replace('.', '').strip()
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo el precio. Se devuelve None " + str(ex))
            return None

    def _get_superficie(self, html: str, parser: BeautifulSoup):
        try:
            s = self._get_feature(html, parser, 'm2')
            s = s.lower().replace('desde', '').strip()
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo la superficie. Se devuelve None " + str(ex))
            return None

    def _get_habitaciones(self, html: str, parser: BeautifulSoup):
        try:
            s = self._get_feature(html, parser, 'hab.')
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo el número de habitaciones. Se devuelve None " + str(ex))
            return None

    def _get_baños(self, html: str, parser: BeautifulSoup):
        try:
            s = self._get_feature(html, parser, 'baños')
            if s == '?':
                s = self._get_feature(html, parser, 'baño')
            if s == '?':
                s = None
            return s
        except Exception as ex:
            self._logger.error("Error obteniendo el número de baños. Se devuelve None " + str(ex))
            return None

    def _get_feature(self, html: str, parser: BeautifulSoup, ends_with: str):
        features = parser.select("#js-feature-container ul li")
        s = ''
        for feature in features:
            ss: str = feature.text.strip()
            if ss.lower().endswith(ends_with.lower()):
                s = ss.lower().replace(ends_with.lower(), '').strip()
                break
        if s == '':
            s = None
        return s

    def _get_total_index_pages(self, html):
        parser = BeautifulSoup(html, 'html.parser')
        paginator = parser.select(".pagination ul li")
        paginator.reverse()
        last_page_tag = paginator[2]
        last_page = last_page_tag.select("a")[0].text
        return last_page

    def _descargar_indice(self):
        html = self._descargar_url(self._current_url)
        return html

    def _descargar_url(self, url):
        html = self._http_client.get(url)  # <- L'objecte _http_client s'encarrega de la gestió d'errors i espaiat de peticions
        return html

    def write_to_csv(self, filename):
        self._logger.info('Escribiendo CSV en ' + filename + '...')
        try:
            self._data.to_csv(filename, ';',  encoding="UTF-16LE")
        except Exception as ex:
            self._logger.error("No es posible guardar los datos en un csv." + str(ex))
            
        self._logger.info('- OK -')
