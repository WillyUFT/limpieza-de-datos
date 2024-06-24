###################
# ! Williams Durán
# ! Limpieza de datos

# * ---------------------------- IMPORTACIONES ---------------------------- #
import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict
import logging

# * ------------------------ CONFIGURACIÓN DE LOGS ------------------------ #
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Logs.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format="Hora: %(asctime)s; Tipo: %(levelname)s; Mensaje: %(message)s;",
                    datefmt="%d-%m-%Y %H:%M:%S")

# * -------------------------- FUNCIÓN PRINCIPAL -------------------------- #
def obtener_datos_base(soup) -> Dict[str, str]:
        
    # & Este h3 contiene como el título del character info, por lo que
    # & podemos ubicar la tabla de información del personaje con él
    h3_personaje_info = soup.find("h3", string="Character Information")
    
    if h3_personaje_info:
                
        # & Acá extraemos la tabla que contiene los datos base
        tabla_datos = h3_personaje_info.find_next("table", class_ = "a-table")
        
        if tabla_datos:
            
            logger.info("Encontramos la tabla de información, comenzando extracción de datos")
            
            # & Extraemos el nombre
            fila_nombre = tabla_datos.find_next("tr")
            nombre_dict = {'Nombre': fila_nombre.find("th").text.strip()}
            
            logger.info("Nombre encontrado: %s", fila_nombre.find("th").text.strip())
            
            # & Extraemos el resto de filas
            filas = tabla_datos.find_all("tr")
            
            # & Extraemos los datos del resto de filas
            info_personaje = extraer_datos_tabla(filas)
            
            # & Juntamos los dos diccionarios y lo retornamos
            return {**nombre_dict, **info_personaje}
        
    else:
        
        logger.error("No se ha podido obtener los datos base del personaje")
        return  {
        "Nombre": "-",
        "Elemento": "-",
        "Rating": "-",
        "Tipo de arma": "-",
        "Rareza": "-",
        "Actor de voz EN": "-",
        "Actor de voz JP": "-"
    }


# * ------------------------- EXTRACCIÓN DE DATOS ------------------------- #
def extraer_datos_tabla(filas: List[Tag]) -> Dict[str, str]:
    
    # & Estos son los datos que retornaremos en forma de diccionario
    rating = ""
    rareza = ""
    elemento = ""
    tipo_arma = ""
    jp_seiyuu = ""
    en_seiyuu = ""
    
    for fila in filas:
                
        # & la tabla está como traspuesta, entonces, el th, que está dentro
        # & del tr, contiene el nombre de la información, mientras que el 
        # & td contiene la información como tal (ver imágen):
        # & imagen tabla_th_td
        th_td = fila.find_all(["th","td"])
        
        if len(th_td) > 1:
                                
            # & Extraemos el encabezado
            encabezado = th_td[0].text.strip()
            
            # & Si estamos en el rating, lo extremos
            if (len(th_td) > 2 and 'rowspan' in th_td[0].attrs and th_td[1].text.strip() == "Rating") or th_td[0].text.strip() == "Rating":
                                
                rating = extraer_rating(th_td)
                logger.info("Rating encontrado: %s", rating)
            
            # & Si estamos en el elemento, lo extremos
            elif encabezado == "Element":
                elemento = th_td[1].text.strip()
                logger.info("Elemento encontrado: %s", elemento)
            
            # & Si estamos en la rareza, la extremos
            elif encabezado == "Rarity": 
                rareza = th_td[1].text.strip()
                logger.info("Rareza encontrada: %s", rareza)
            
            # & Si estamos en el tipo de arma, lo extremos
            elif encabezado == "Weapon":
                tipo_arma = th_td[1].text.strip()
                logger.info("Tipo de arma encontrada: %s", tipo_arma)
            
            # & Si estamos en los actores, los extraemos
            elif encabezado == "Voice Actors":
                en_seiyuu = extraer_actriz_en(th_td[1])    
                logger.info("Actor de voz en inglés encontrado: %s", en_seiyuu)
                jp_seiyuu = extraer_actriz_jp(th_td[1])
                logger.info("Actor de voz en japonés encontrado: %s", jp_seiyuu)
    
    # & Armamos el diccionario
    diccionario = {
        "Elemento": elemento,
        "Rating": rating,
        "Tipo de arma": tipo_arma,
        "Rareza": rareza,
        "Actor de voz EN": en_seiyuu,
        "Actor de voz JP": jp_seiyuu
    }
    
    return diccionario


# * -------------------- EXTRACCIÓN DE ACTOR EN INGLÉS -------------------- #
def extraer_actriz_en(actrices: List[Tag]) -> str:
        
    en_seiyuu = ""
                    
    # & Cómo las actrices vienen juntas y simplemente están separadas por un
    # & <br> tendremos que buscar un método un poco más agresivo para obtenerlas
    # & seiyuu_br
    for contenido in actrices.contents:
        
        # & Formato para personajes más antiguos
        if isinstance(contenido, str) and "EN Voice Actor" in contenido:
            en_seiyuu = contenido.replace("EN Voice Actor: ", "").strip()
            
        # & Formato de personajes nuevos
        elif isinstance(contenido, str) and "(EN)" in contenido:
            en_seiyuu = contenido.replace("(EN)", "").strip()
            
    return en_seiyuu


# * -------------------- EXTRACCIÓN DE ACTOR EN JAPONÉS ------------------- #
def extraer_actriz_jp(actrices: List[Tag]) -> str:
        
    jp_seiyuu = ""
                    
    # & Cómo las actrices vienen juntas y simplemente están separadas por un
    # & <br> tendremos que buscar un método un poco más agresivo para obtenerlas
    # & seiyuu_br
    for contenido in actrices.contents:
        
        # & Formato para personajes más antiguos
        if isinstance(contenido, str) and "JP Voice Actor" in contenido:
            jp_seiyuu = contenido.replace("JP Voice Actor: ", "").strip()
            
        # & Formato de personajes nuevos
        elif isinstance(contenido, str) and "(JP)" in contenido:
            jp_seiyuu = contenido.replace("(JP)", "").strip()
            
    return jp_seiyuu
   
# * ------------------------- EXTACCIÓN DE RATING ------------------------- #
def extraer_rating(th_td: List[Tag]) -> str:

    # & Así, a veces tenemos tres columnas dentro de la fila, cómo se ve en la imagen
    # & tres_columnas_rating 
    if len(th_td) > 2 and 'rowspan' in th_td[0].attrs and th_td[1].text.strip() == "Rating":
        
        # & Sacamos el rating
        icon = th_td[2].find("img")
        if icon and 'alt' in icon.attrs:
            return icon['alt'].replace(" Rank Icon", "")

    # & Sacamos el rating para situaciones normales, menos mal!
    # & rango_alt
    elif th_td[0].text.strip() == "Rating":
        icon = th_td[1].find("img")
        if icon and 'alt' in icon.attrs:
            return icon['alt'].replace(" Rank Icon", "")