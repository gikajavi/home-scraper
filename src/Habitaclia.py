import random
from bs4 import BeautifulSoup
from log_helper import LogHelper
from http_helper import HttpHelper


class HabitacliaScraper():
    def __init__(self):
        self.url = "https://www.habitaclia.com/alquiler-barcelona.htm"
        self.dataset = []
        self.session_id = "sess-" + str(random.random())
        self._log_helper = LogHelper("./logs/log-" + self.session_id)
        self._http_helper = HttpHelper(self._log_helper, 5, 2)
        self._log("Habitaclia Scraper Iniciado")

    def start(self):
        html_code = self._descargar_indice()
        self.total_index_pages = int(self._get_total_index_pages(html_code))
        # Scraping del índice principal:
        url_to_scrap = self.get_url_to_scrap_by_index(0)
        self.scrap_index_page(url_to_scrap)
        # Scraping para el resto de índices (según la paginación)
        i = 1
        while i < self.total_index_pages:
            url_to_scrap = self.get_url_to_scrap_by_index(i)
            self.scrap_index_page(url_to_scrap)
            i += 1;

    def get_url_to_scrap_by_index(self, index):
        if index == 0:
            return self.url
        else:
            to_scrap = self.url
            return to_scrap.replace('.htm', "-" + str(index) + '.htm')

    def scrap_index_page(self, url):
        try:
            self._log("Index scraping en " + url)
            html = self._descargar_url(url)
            parser = BeautifulSoup(html, 'html.parser')
            links = parser.select(".list-item-title a")
            for link in links:
                data_url = link['href'];
                self.scrap_data_page(data_url)
        except Exception as ex:
            self._log("Error en el index scraping " + str(ex))

    def scrap_data_page(self, url):
        try:
            self._log("Data scraping en " + url)

            # Algunes poques ofertes són de fotocasa i habitaclia ja indica que la major part de la info. està allí.
            # No ens interessen per manca de qualitat (dades insuficients)
            if self._fotocasa_id(url):
                self._log("URL descartada (falta de datos)")
                return

            html = self._descargar_url(url)
            parser = BeautifulSoup(html, 'html.parser')

            # Se obtienen de la URL
            housing_id = self._get_housing_id_by_url(url)
            tipus = self._get_housing_type_by_url(url)

            # Se obtienen de la sección "summary"
            municipi = self._get_municipio(parser)
            barri = self._get_barrio(parser)
            preuactual = self._get_precio(parser)
            superficie = self._get_superficie(html, parser)
            habitaciones = self._get_habitaciones(html, parser)
            baños = self._get_baños(html, parser)

            # Se obtienen de "Características generales"
            antiguedad = self._get_antiguedad(parser)
            planta = self._get_planta(parser)
            parking = 'No'
            if self._general_feature_exists("Plaza parking", parser):
                parking = 'Sí'
            calefaccio = 'No'
            if self._general_feature_exists("Calefacción", parser):
                calefaccio = 'Sí'
            aire_acondicionat = 'No'
            if self._general_feature_exists("Aire acondicionado", parser):
                aire_acondicionat = 'Sí'
            moblat = 'Sí'
            if self._general_feature_exists("Sin amueblar", parser):
                moblat = 'No'
            # Etiquetat eficiència energètica i d'emissions
            eti_consum = self._get_eti_eficiencia(parser)
            eti_emissions = self._get_eti_emissions(parser)

            # Se obtienen de "Equipamiento comunitario"
            jardi = 'No'
            if self._community_feature_exists("Jardín", parser):
                jardi = 'Sí'
            ascensor = 'No'
            if self._community_feature_exists("Ascensor", parser):
                ascensor = 'Sí'

            r = dict()
            r['Id'] = housing_id
            r['Url'] = url
            r['Tipus'] = tipus
            r['Municipi'] = municipi
            r['Barri'] = barri
            r['Preu Actual (€)'] = preuactual
            r['Superfície (m2)'] = superficie
            r['#Habitacions'] = habitaciones
            r['#Banys'] = baños
            r['Antiguitat'] = antiguedad
            r['Planta'] = planta
            r['Parking'] = parking
            r['Calefacció'] = calefaccio
            r['Aire acondicionat'] = aire_acondicionat
            r['Moblat'] = moblat
            r['Eficiència energètica'] = eti_consum
            r['Classe emissions'] = eti_emissions
            r['Jardi'] = jardi
            r['Ascensor'] = ascensor
            self.dataset.append(r.copy())
            return
        except Exception as ex:
            self._log("Error en el data scraping " + str(ex))

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
            return '?'
        except Exception as ex:
            self._log("Error obteniendo la etiqueta de eficiencia energética. Se devuelve ? " + str(ex))
            return '?'

    def _get_eti_emissions(self, parser: BeautifulSoup):
        try:
            eles = parser.select('.detail-rating .rating-box')
            for ele in eles:
                s: str = ele.text
                if s.lower().strip().startswith('emisiones'):
                    o: str = ele.select('.rating')[0].text
                    return o.strip()
            return '?'
        except Exception as ex:
            self._log("Error obteniendo la etiqueta de emisiones. Se devuelve ? " + str(ex))
            return '?'

    def _get_antiguedad(self, parser: BeautifulSoup):
        try:
            ele = self._get_general_ele(parser)
            if not ele:
                return '?'
            items = ele.select('ul li')
            for item in items:
                s = str(item.text).lower().strip()
                if s.startswith('año construcción'):
                    planta = s.replace('año construcción', '').strip()
                    return planta
            return '?'
        except Exception as ex:
            self._log("Error obteniendo la antigüedad. Se devuelve ? " + str(ex))
            return '?'

    def _get_planta(self, parser: BeautifulSoup):
        try:
            ele = self._get_general_ele(parser)
            if not ele:
                return '?'
            items = ele.select('ul li')
            for item in items:
                s = str(item.text).lower().strip()
                if s.startswith('planta número'):
                    planta = s.replace('planta número', '').strip()
                    return planta
            return '?'
        except Exception as ex:
            self._log("Error obteniendo la planta. Se devuelve ? " + str(ex))
            return '?'

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
            self._log("Error obteniendo la característica general " + feature + " Se considerará que no existe " + str(ex))
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
            self._log("Error obteniendo la característica de comunidad " + feature +
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
            self._log("Error obteniendo el Id de la oferta " + str(ex) + " Se aborta el scraping de esta URL")
            raise

    def _get_housing_type_by_url(self, url):
        try:
            l = url.split('/')
            suff: str = str(l[3]).lower()
            if suff.startswith('alquiler-piso') or suff.startswith('alquiler-apartamento'):
                return 'piso'
            if suff.startswith('alquiler-casa'):
                return 'casa'
            if suff.startswith('alquiler-duplex'):
                return 'duplex'
            if suff.startswith('alquiler-atico'):
                return 'atico'
            return 'otros'
        except Exception as ex:
            self._log("Error obteniendo el tipo de inmueble " + str(ex) + " Se aborta el scraping de esta URL")
            raise

    def _get_municipio(self, parser: BeautifulSoup):
        # v1 només Bcn:
        return 'Barcelona'

    def _get_barrio(self, parser: BeautifulSoup):
        try:
            s = parser.select("article.location h4 a")[0].text.strip()
            return s
        except Exception as ex:
            self._log("Error obteniendo el barrio. Se devuelve ? " + str(ex))
            return '?'

    def _get_precio(self, parser: BeautifulSoup):
        try:
            s = parser.select(".summary .price span[itemprop=price]")[0].text.strip()
            s = s.replace('€', '').replace('.', '').strip()
            return s
        except Exception as ex:
            self._log("Error obteniendo el precio. Se devuelve ? " + str(ex))
            return '?'

    def _get_superficie(self, html: str, parser: BeautifulSoup):
        try:
            s = self._get_feature(html, parser, 'm2')
            s = s.lower().replace('desde', '').strip()
            return s
        except Exception as ex:
            self._log("Error obteniendo la superficie. Se devuelve ? " + str(ex))
            return '?'

    def _get_habitaciones(self, html: str, parser: BeautifulSoup):
        try:
            s = self._get_feature(html, parser, 'hab.')
            return s
        except Exception as ex:
            self._log("Error obteniendo el número de habitaciones. Se devuelve ? " + str(ex))
            return '?'

    def _get_baños(self, html: str, parser: BeautifulSoup):
        try:
            s = self._get_feature(html, parser, 'baños')
            if s == '?':
                s = self._get_feature(html, parser, 'baño')
            return s
        except Exception as ex:
            self._log("Error obteniendo el número de baños. Se devuelve ? " + str(ex))
            return '?'

    def _get_feature(self, html: str, parser: BeautifulSoup, ends_with: str):
        features = parser.select("#js-feature-container ul li")
        s = ''
        for feature in features:
            ss: str = feature.text.strip()
            if ss.lower().endswith(ends_with.lower()):
                s = ss.lower().replace(ends_with.lower(), '').strip()
                break
        if s == '':
            s = '?'
        return s

    def _get_total_index_pages(self, html):
        parser = BeautifulSoup(html, 'html.parser')
        paginator = parser.select(".pagination ul li")
        paginator.reverse()
        last_page_tag = paginator[2]
        last_page = last_page_tag.select("a")[0].text
        return last_page

    def _descargar_indice(self):
        html = self._descargar_url(self.url)
        return html

    def _log(self, s):
        self._log_helper.write(s)

    def _descargar_url(self, url):
        html = self._http_helper.get(url)
        return html

    def write_to_csv(self, filename):
        self._log('Escribiendo CSV en ' + filename + '...')
        f = open(filename, "w+")
        hdr_written = False
        for d in self.dataset:
            if not hdr_written:
                for k in d:
                    f.write(k + ";")
                f.write("\n")
                hdr_written = True
            for k in d:
                f.write(d[k] + ";")
            f.write("\n")
        f.close()
        self._log('- OK -')
