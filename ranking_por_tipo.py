###################
# ! Williams Durán
# ! Limpieza de datos

# * ---------------------------- IMPORTACIONES ---------------------------- #
import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict

# * ------------------------ CONFIGURACIÓN DE LOGS ------------------------ #
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Logs.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format="Hora: %(asctime)s; Tipo: %(levelname)s; Mensaje: %(message)s;",
                    datefmt="%d-%m-%Y %H:%M:%S")

# * -------------------------- FUNCIÓN PRINCIPAL -------------------------- #
# ~ Función principal, trae la tabla  de los ranking en base a su 
# ~ desempeño en ciertos ámbitos.
# ~ tabla_tier_list_ej
def obtener_tabla_list_ranking(soup) -> Dict[str, str]:
      
    # & Este h4 contiene el título de "Tier List Rankings", por lo que
    # & con esto podemos ubicar la tabla de información acerca del 
    # & desempeño del personaje
    h4_tier_list_info = soup.find("h4", string="Tier List Rankings")
    
    if h4_tier_list_info:
        
        # & Extramos la tabla del tier list
        tabla_datos = h4_tier_list_info.find_next("table", class_ = "a-table")
        
        if tabla_datos:
            
            logger.info('Encontramos la tabla de información, se procede a extraer la información')
            
            filas = tabla_datos.find_all("tr")
            
            tier_list = extraer_datos_tabla(filas)
            
            return tier_list
    
    else:
        
        return {
            'Main DPS': "-",
            'Sub-DPS': "-",
            'Support': "-",
            'Exploración': "-"
        }


# * ------------------------- EXTRACCIÓN DE DATOS ------------------------- #
# ~ Para no tener una función con tanta complejidad arriba, sacaremos los datos
# ~ en esta función y luego retornaremos un diccionario a la función principal.
# ~ Esta tabla no está traspuesta como la anterior, así que será mucho más fácil
# ~ de leer, lo que haremos será leer únicamente la fila que contiene los rankings,
# ~ como todos los personajes tienen este formato de tabla, simplemente leeremos la fila
# ~ de izquierda a derecha, donde Main DPS siempre será el primero y Exploration
# ~ siempre será el último.
# ~ tabla_tier_list_formato
def extraer_datos_tabla(filas: List[Tag]) -> Dict[str, str]:
    
    # & Estos son los datos que retornaremos en forma de diccionario
    main_dps = ""
    sub_dps = ""
    support = ""
    exploration = ""
    
    # & Esta es la fila que contiene la información
    fila_tier_list = filas[1]
    
    # & Acá extramos todos los td que contiene la fila 
    td_fila = fila_tier_list.find_all("td")
    
    for td in range (0, len(td_fila)):
        if td == 0:
            main_dps = extraer_rating(td_fila[0])
            logger.info("Rating como Main DPS encontrado %s", main_dps)
        elif td == 1:
            sub_dps = extraer_rating(td_fila[1])
            logger.info("Rating como Sub-DPS encontrado %s", sub_dps)
        elif td == 2:
            support = extraer_rating(td_fila[2])
            logger.info("Rating como Support encontrado %s", support)
        elif td == 3:
            exploration = extraer_rating(td_fila[3])
            logger.info("Rating como Exploración encontrado %s", exploration)
            
    diccionario = {
        'Main DPS': main_dps,
        'Sub-DPS': sub_dps,
        'Support': support,
        'Exploración': exploration
    }
    return diccionario
    

# * ------------------------- EXTRAER INFO DE IMG ------------------------- #
# ~ Usaremos esta función para no repetirnos, acá traemos el td que debería contener
# ~ la información que queremos, para ello, verificamos si existe una imagen, si existe,
# ~ extraemos el atributo alt de esta, que nos describe el tier. En caso de que 
# ~ no tengamos imágenes, simplemente leermos el texto, que traerá un -.
def extraer_rating(td: Tag) -> str:
    
    icono = td.find("img")
    
    if icono and 'alt' in icono.attrs:
        return icono['alt'].strip()
    else:
        return td.text.strip()