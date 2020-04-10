###
# Copyright (c) 2020, Leonel Faria
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('COVID19')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x
import urllib.parse
from urllib.request import urlopen, HTTPError, URLError
from datetime import datetime as dt
from datetime import timedelta
import datetime
import re
import requests
import urllib.request
import json
from bs4 import BeautifulSoup


class COVID19(callbacks.Plugin):
    """COVID19 Live Status"""
    def covid19(self, irc, msg, args, argv):
        """<COVID19>
        Returns the current world wide COVID19 cases (Worldmeters.info).
        """
        url = 'https://www.worldometers.info/coronavirus/'
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        country = 'Total:'
        content = urllib.request.urlopen(req)
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", id='main_table_countries_today')
        if not table:
            irc.error("Data source is unreachable")
            return
        else:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]   
                if (len(row) > 0):  
                    if (country.lower() == row[0].lower().strip()):
                        deaths = "0"
                        new = "0"
                        ndeaths = "0"
                        if (len(row[3]) > 1):
                            deaths = row[3].strip()
                        if (len(row[4]) > 1):
                            ndeaths = row[4].strip()
                        if (len(row[2]) > 1):
                            new = row[2].strip()
                        output = "Cases Worldwide: " + row[1].strip() + " (new " + new + ") Total deaths: " + deaths + " (new " + ndeaths + ") Recovered: " + row[5].strip() + " Active cases: " + row[6].strip() + " Serious/Critical: " + row[7].strip()
            irc.reply(output, prefixNick=False)
    covid19 = wrap(covid19, [additional('text')])
    def covid19y(self, irc, msg, args, argv):
        """<COVID19>
        Returns the yesterday world wide COVID19 cases (Worldmeters.info).
        """
        url = 'https://www.worldometers.info/coronavirus/'
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        country = 'Total:'
        content = urllib.request.urlopen(req)
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", id='main_table_countries_yesterday')
        if not table:
            irc.error("Data source is unreachable")
            return
        else:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]   
                if (len(row) > 0):  
                    if (country.lower() == row[0].lower().strip()):
                        deaths = "0"
                        new = "0"
                        ndeaths = "0"
                        if (len(row[3]) > 1):
                            deaths = row[3].strip()
                        if (len(row[4]) > 1):
                            ndeaths = row[4].strip()
                        if (len(row[2]) > 1):
                            new = row[2].strip()
                        output = "Cases Worldwide (yesterday): " + row[1].strip() + " (new " + new + ") Total deaths: " + deaths + " (new " + ndeaths + ") Recovered: " + row[5].strip() + " Active cases: " + row[6].strip() + " Serious/Critical: " + row[7].strip()
            irc.reply(output, prefixNick=False)
    covid19y = wrap(covid19y, [additional('text')])
    def fcovid19(self, irc, msg, args, argv):
        """<COVID19>
        Returns the current COVID19 cases in <Country> (Worldmeters.info).
        """
        argv2 = str(argv).split(" ")
        if (len(argv2) < 1):
            irc.error("Usage .fcovid19 <country>")
            return
        if (len(argv2) >= 1):
            country = argv
        else:
            country = argv[0]
        output = 'Not found'
        
        url = 'https://www.worldometers.info/coronavirus/'
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        content = urllib.request.urlopen(req)
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", id='main_table_countries_today')
        if not table:
            irc.error("Data source is unreachable")
            return
        else:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]   
                if (len(row) > 0):  
                    if (country.lower() == row[0].lower().strip()):
                        deaths = "0"
                        new = "0"
                        ndeaths = "0"
                        if (len(row[3]) > 1):
                            deaths = row[3].strip()
                        if (len(row[4]) > 1):
                            ndeaths = row[4].strip()
                        if (len(row[2]) > 1):
                            new = row[2].strip()
                        output = "Cases in " + row[0].strip() + ": " + row[1].strip() + " (new " + new + ") Total deaths: " + deaths + " (new " + ndeaths + ") Recovered: " + row[5].strip() + " Active cases: " + row[6].strip() + " Serious/Critical: " + row[7].strip()
            irc.reply(output, prefixNick=False)
    fcovid19 = wrap(fcovid19, [additional('text')])
    def fcovid19y(self, irc, msg, args, argv):
        """<COVID19>
        Returns the yesterday COVID19 cases in <Country> (Worldmeters.info).
        """
        argv2 = str(argv).split(" ")
        if (len(argv2) < 1):
            irc.error("Usage .fcovid19 <country>")
            return
        if (len(argv2) >= 1):
            country = argv
        else:
            country = argv[0]
        output = 'Not found'
        url = 'https://www.worldometers.info/coronavirus/'
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        content = urllib.request.urlopen(req)
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", id='main_table_countries_yesterday')
        if not table:
            irc.error("Data source is unreachable")
            return
        else:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]   
                if (len(row) > 0):  
                    if (country.lower() == row[0].lower().strip()):
                        deaths = "0"
                        new = "0"
                        ndeaths = "0"
                        if (len(row[3]) > 1):
                            deaths = row[3].strip()
                        if (len(row[4]) > 1):
                            ndeaths = row[4].strip()
                        if (len(row[2]) > 1):
                            new = row[2].strip()
                        output = "Cases in " + row[0].strip() + " (Yesterday): " + row[1].strip() + " (new " + new + ") Total deaths: " + deaths + " (new " + ndeaths + ") Recovered: " + row[5].strip() + " Active cases: " + row[6].strip() + " Serious/Critical: " + row[7].strip()
            irc.reply(output, prefixNick=False)
    fcovid19y = wrap(fcovid19y, [additional('text')])
    def cv19pt(self, irc, msg, args, argv):
        """<COVID19>
        Returns the current COVID19 Data for Portugal (Data from DGS).
        """
        output = 'Not found'
        url = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19Portugal_UltimoRel/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&resultOffset=0&resultRecordCount=50&cacheHint=true'
        req = urllib.request.Request(
            url, 
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        try:
            response = urlopen(req)
        except (HTTPError, URLError) as error:
            irc.error('Data of %s not retrieved because %s', name, error)  
            return
        except timeout:
            irc.error('Socket timed out, please try again later') 
            return
        values = json.loads(response.read().decode('utf-8'))
        valdat = values['features'][0]['attributes']
        datarelatorio = dt.fromtimestamp(int(str(valdat['datarelatorio'])[0:10]))
        output = "Dados DGS Casos Confirmados: " + str(valdat['casosconfirmados']) + " (" + str(valdat['casosnovos']) + " novos) | Internados: " + str(valdat['CasosInternados']) + " | Internados UCI: " + str(valdat['CasosInternadosUCI']) + " | Casos suspeitos: " + str(valdat['casossuspeitos']) + " | Recuperados: " + str(valdat['recuperados']) + " | Aguardam resultado de Lab.: " + str(valdat['AguardaReslab']) + " | Obitos: " + str(valdat['nrobitos']) + " | Data do relatório: " + str(datarelatorio)
        irc.reply(output, prefixNick=False)
    cv19pt = wrap(cv19pt, [additional('text')])
    def fcv19pt(self, irc, msg, args, argv):
        """<COVID19>
        Returns the current COVID19 Data for Portugal Cities (Data DGS).
        """
        argv2 = str(argv).split(" ")
        if (len(argv2) < 1):
            irc.error("Usage .fcv19pt <concelho>")
            return
        if (len(argv2) >= 1):
            fcidade = argv
        else:
            fcidade = argv[0]
        output = 'Not found'
        url = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/CAOP_COVID3003_view/FeatureServer/0/query?f=json&where=CasosConfirmados3003%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=CasosConfirmados3003%20desc&resultOffset=0&resultRecordCount=390&cacheHint=true'

        req = urllib.request.Request(
            url, 
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        try:
            response = urlopen(req)
        except (HTTPError, URLError) as error:
            irc.error('Data of %s not retrieved because %s', name, error)  
            return
        except timeout:
            irc.error('Socket timed out, please try again later') 
            return
        values = json.loads(response.read().decode('utf-8'))
        valdat = values['features']
        resultado = ""
        for concelho in valdat:
            if (concelho['attributes']['Concelho'].lower() == fcidade.lower()):
                resultado = concelho['attributes']
        if (resultado == ""):
            output = "Não foram encontrados resultados"
        else:
<<<<<<< HEAD
            datarelatorio = datetime.fromtimestamp(int(str(valdat['Data_Conc'])[0:10]))
            output = "Dados DGS Casos Confirmados acumulados (" + str(resultado['Concelho']).lower().capitalize() + "): " + str(resultado['ConfirmadosAcumulado_Conc']) + " | Recuperados: " + str(resultado['Recuperados_Conc']) + " | Obitos: " + str(resultado['Obitos_Conc']) + " | Data do relatório: " + str(datarelatorio)
=======
            today = datetime.date.today().day
            yesterday = datetime.date.today() - timedelta(1)
            dayStr = '{:02d}'.format(today) + '{:02d}'.format(datetime.date.today().month)
            dayYStr = '{:02d}'.format(yesterday.day) + '{:02d}'.format(yesterday.month)
            valores = dict()
            for data in resultado:
                if (data.startswith('CasosConfirmados')):
                    if (resultado[data] != None):
                        valores[data.replace('CasosConfirmados','')] = resultado[data]
            if (dayStr in valores):
                valor = valores[dayStr]
                valory = valores[dayYStr]
            else:
                lvalores = list(valores.values())
                valor = lvalores[-1]
                valory = lvalores[-2]
            lkeys = list(valores)
            novos = int(valor) - int(valory)
            if (novos > 0):
                novos = "+" + str(novos)
            else:
                novos = str(novos)
            data_dados = lkeys[-1][0:2] + "/" + lkeys[-1][2:4]
            output = "Dados DGS Casos Confirmados (" + str(resultado['Concelho_min']) + "): " + str(valor) + " (novos " + novos + ") Dados relativos a " + data_dados
>>>>>>> 9418def714bdba643f083fe28006c03067908b6c
        irc.reply(output, prefixNick=False)
    fcv19pt = wrap(fcv19pt, [additional('text')])
Class = COVID19
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79: