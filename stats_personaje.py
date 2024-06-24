###################
# ! Williams Durán
# ! Limpieza de datos

# * ---------------------------- IMPORTACIONES ---------------------------- #
import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict
import re 

# * ------------------------ CONFIGURACIÓN DE LOGS ------------------------ #
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Logs.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format="Hora: %(asctime)s; Tipo: %(levelname)s; Mensaje: %(message)s;",
                    datefmt="%d-%m-%Y %H:%M:%S")

# * -------------------------- FUNCIÓN PRINCIPAL -------------------------- #
# ~ Función principal, que trae la tabla de las stats del personaje
# ~ En esta creamos la sopita para encontrar el h3 que tiene el título Stats en
# ~ ella, por ejemplo "Raiden's stats", sin embargo, no todos los personajes se 
# ~ llaman igual, así que ocuparemos una expresión regular para encontrarlo. 
# ~ Luego llamaremos a las funciones que extraerán la información de cada fila.
# ~ Sin embargo, acá tenemos una tabla doble, una que está activa y otra que no,
# ~ Por lo que lo haremos por separado para no sobrecargar esta función.
# ~ tabla_stats_ej
def obtener_tabla_stats(soup) -> Dict[str, str]:
    
    # & Este h3 contiene como el título del character info, por lo que
    # & podemos ubicar la tabla de información del personaje con él
    h3_personaje_stats = soup.find("h3", string=re.compile(".*Stats.*"))
    
    if h3_personaje_stats:
        
        # & Acá nos encontramos con un problema, porque hay una tabla oculta y 
        # & otra activa, por defecto viene activa la de los valores mínimos, mientras
        # & que la de valores máximos viene oculta, así que vamos a extraerlas
        # & por separado
        # & tabla_stats_formato
        
        logger.info('Encontramos el div que contiene las tablas, se procede a extraer la información')
        
        div_base = h3_personaje_stats.find_next("div", class_ = "a-tabPanel is-active")
        div_max = div_base.find_next("div", class_ = "a-tabPanel")

        logger.info('Buscando las stats base')        
        diccionario_stats_base = obtener_stats(div_base)
        
        logger.info('Buscando las stats máximas')
        diccionario_stats_max = obtener_stats(div_max)
        
        diccionario_stats_base =  {f"Base {key}": value for key, value in diccionario_stats_base.items()}
        diccionario_stats_max = {f"Max {key}": value for key, value in diccionario_stats_max.items()}

        return {**diccionario_stats_base, **diccionario_stats_max}

# ~ Esta función toma el div que contiene la tabla que queremos analizar
# ~ y luego retornará los valores que contiene.
def obtener_stats(div: Tag) -> Dict[str, str]:
    
    # & Estos son los datos que retornaremos en forma de diccionario
    vida = ""
    ataque = ""
    defensa = ""
    
    tabla = div.find_next("table", class_ = "a-table")
    
    if tabla:
        
        filas = tabla.find_all("tr")
                   
        for fila in filas:
            
            th_td = fila.find_all(["th", "td"])
                                
            # & Extraemos el encabezado
            encabezado = th_td[0].text.strip()
            
            if encabezado == "HP":
                vida = th_td[1].text.strip()
                logger.info("HP encontrada %s", vida)
            elif encabezado == "ATK":
                ataque = th_td[1].text.strip()
                logger.info("ATK encontrado %s", ataque)
            elif encabezado == "DEF":
                defensa = th_td[1].text.strip()
                logger.info("DEF encontrada %s", defensa)
                
    diccionario = {
        'HP': vida,
        'ATK': ataque,
        'DEF': defensa
    }
    return diccionario