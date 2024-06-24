###################
# ! Williams Durán
# ! Limpieza de datos

# * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Importaciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
import pandas as pd
import info_base
import ranking_por_tipo
import stats_personaje
import requests
import logging
from bs4 import BeautifulSoup, Tag
from typing import List, Dict
import time
import os
import json

# * ------------------------ CONFIGURACIÓN DE LOGS ------------------------ #
logger = logging.getLogger(__name__)
logging.basicConfig(filename='Logs.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format="Hora: %(asctime)s; Tipo: %(levelname)s; Mensaje: %(message)s;",
                    datefmt="%d-%m-%Y %H:%M:%S")

# * ------------------------------- PROGRESO ------------------------------ #
def guardar_progreso(progreso, archivo_progreso):
    with open(archivo_progreso, 'w') as f:
        json.dump(progreso, f)

def cargar_progreso(archivo_progreso):
    if os.path.exists(archivo_progreso):
        try:
            with open(archivo_progreso, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("No tenemos progreso. Iniciando desde el principio.")
            return {'ultimo_personaje': -1, 'datos_personajes': []}
    return {'ultimo_personaje': -1, 'datos_personajes': []}

def buscar_info_personajes() -> None:
    
    # & Traemos el archivo del progreso, para ver si lo tenemos
    archivo_progreso = 'progreso_scraping.json'
    
    progreso = cargar_progreso(archivo_progreso)
    ultimo_personaje = progreso['ultimo_personaje']
    datos_personajes = progreso['datos_personajes']
    
    # & Acá comenzamos la recolección de tiempo y recursos que cuesta esta función
    tiempo_inicio_total = time.time()
    tamanio_total_analizado = 0
    velocidad_transferencia_promedio = 0
    
    logger.info("Iniciando extracción de los datos")
    
    # & Traemos el excel en modo pandas
    df = pd.read_excel('Genshin_Impact_Characters.xlsx')

    for personaje in range(ultimo_personaje + 1, len(df)):
        
        tiempo_inicio_personaje = time.time()
        
        nombre = df.iloc[personaje]['Name']    
        link = df.iloc[personaje]['URLS']

        # & Obtenemos la sopita de la página de cada personaje
        logger.info("%s: Obteniendo información del personaje", nombre)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, "lxml")  
        
        # & Buscamos la información base del personaje
        logger.info("%s: Obteniendo información base del personaje", nombre)
        datos_base = info_base.obtener_datos_base(soup)
        logger.info("%s: Información base obtenida", nombre)
        
        # & Buscamos el rating del personaje
        logger.info("%s: Obteniendo rating del personaje según su desempeño", nombre)
        ranking = ranking_por_tipo.obtener_tabla_list_ranking(soup)
        logger.info("%s: Rating del personaje obtenido", nombre)
        
        # & Buscamos las stats del personaje
        logger.info("%s: Obteniendo stats del personaje", nombre)
        stats = stats_personaje.obtener_tabla_stats(soup)
        logger.info("%s: Stats del personaje obtenidas", nombre)
        
        # & Juntamos los dataframes en solo uno
        datos_personaje = {**datos_base, **ranking, **stats}
        
        # & Y lo agregamos a la lista que después será un dataframe
        logger.info("%s: Data frame del personaje agregado a la lista", nombre)
        datos_personajes.append(datos_personaje)
        
        # & Guardamos el progreso, en caso de que muera
        progreso = {
            'ultimo_personaje': personaje,
            'datos_personajes': datos_personajes
        }
        guardar_progreso(progreso, archivo_progreso)
        
        tiempo_final_personaje = time.time()
        
        # & Calculamos tiempos y costos de espacio
        tiempo_total_extraccion_personaje = tiempo_final_personaje - tiempo_inicio_personaje
        
        tamanio_raw_request_personaje = len(request.content)
        tamanio_total_analizado += tamanio_raw_request_personaje
        
        velocidad_transferencia_personaje = tamanio_raw_request_personaje/tiempo_total_extraccion_personaje
        velocidad_transferencia_promedio += velocidad_transferencia_personaje
        
        # & Logeamos los datos
        logger.info("%s: Tiempo de adquisición total: %.2f segundos", nombre, tiempo_total_extraccion_personaje)
        logger.info("%s: Cantidad total de datos: %d bytes", nombre, tamanio_raw_request_personaje)
        logger.info("%s: Velociidad de transferencia de datos: %d bytes/segundo", nombre, velocidad_transferencia_personaje)
        
    # & Creamos el DataFrame con los datos recolectados
    columnas = ['Nombre', 'Elemento', 'Rating', 'Tipo de arma', 
                'Rareza', 'Actor de voz EN', 'Actor de voz JP',
                'Main DPS', 'Sub-DPS', 'Support', 'Exploración',
                'Base HP', 'Base ATK', 'Base DEF', 'Max HP', 
                'Max ATK', 'Max DEF']

    df_final = pd.DataFrame(datos_personajes, columns=columnas)

    # &  Guardamos el DataFrame en un archivo Excel
    df_final.to_excel("Genshin_Impact_Characters_Final.xlsx", index=False)
    print(df_final)
    
    tiempo_final_total = time.time()
    
    # & Calculamos tiempos y costos de espacio
    tiempo_total_extraccion = tiempo_final_total - tiempo_inicio_total
    velocidad_transferencia_promedio /= len(df_final)
    cantidad_datos_tabulados_total = os.path.getsize("Genshin_Impact_Characters_Final.xlsx")
    
    # & Logeamos los datos
    logger.info("Tiempo total para adquirir información de los personajes: %.2f segundos" % tiempo_total_extraccion)
    logger.info("Cantidad total de datos raw que se analizaron sumando todos los personajes: %d bytes" % tamanio_total_analizado)
    logger.info("Cantidad de datos tabulados: %d bytes" % cantidad_datos_tabulados_total)
    logger.info("Velocidad de transferencia promedio: %.2f bytes/segundo" % velocidad_transferencia_promedio)
   
def buscar_tabla_lista_personajes() -> None:
    
    # & Obtenemos la URL principal
    url_lista_personaje = "https://game8.co/games/Genshin-Impact/archives/296707"
    logger.info('Vamos a obtener la tabla de la lista de personajes al siguiente link: %s' %url_lista_personaje )
    
    # & Creamos la sopita y obtenemos la tabla
    request = requests.get(url_lista_personaje)
    soup = BeautifulSoup(request.text, "lxml")
    table_principal = soup.find("table", class_ = "a-table a-table a-table flexible-cell")

    # & Comenzamos a tomar el tiempo
    tiempo_inicio = time.time()

    # & Si la tabla existe
    if table_principal:
        
        logger.info("La tabla ha sido encontrada satisfactoriamente!")
        
        # ! Convertimos la tabla HTML en un DataFrame de pandas
        df_principal = pd.read_html(str(table_principal))[0]
        logger.info("Data frame creado con la tabla encontrada")
        
        # ^ Sacamos los headers de la tabla, para poder sacar los links de cada personaje
        rows = table_principal.find_all("tr")[1:]
        
        # ^ Comenzamos a guardar los links en una lista
        urls = []
        
        # ^ Buscamos en la primera columna el link hacia la información del personaje
        logger.info("Extrayendo URL de cada personaje")
        for row in rows:
            first_cell = row.find_all("td")[0]
            link = first_cell.find("a", class_="a-link")
            if link and 'href' in link.attrs:
                urls.append(link['href'])
            else:
                urls.append(None)

        # ^ Agregamos una columna nueva al data frame con los links de cada personaje
        df_principal['URLS'] = urls
        logger.info("El data frame ahora contiene el url de la página de información de cada personaje")
        
        # ^ Guardamos el Excel
        logger.info("Guardando data frame en archivo Excel")
        df_principal.to_excel("Genshin_Impact_Characters.xlsx", index=False)
        logger.info("Data frame exportado a Excel existosamente")
        
        tiempo_final = time.time()
        
        # & Calculamos tiempos y costos de espacio
        tiempo_total_extraccion = tiempo_final - tiempo_inicio
        tamanio_raw_size = len(request.content)
        cantidad_datos_tabulados = os.path.getsize("Genshin_Impact_Characters.xlsx")
        velocidad_transferencia = tamanio_raw_size/tiempo_total_extraccion
        
        # & Logeamos los datos
        logger.info("Tiempo de adquisición total: %.2f segundos" % tiempo_total_extraccion)
        logger.info("Cantidad total de datos raw: %d bytes" % tamanio_raw_size)
        logger.info("Cantidad de datos tabulados: %d bytes" % cantidad_datos_tabulados)
        logger.info("Velocidad de transferencia: %.2f bytes/segundo" % velocidad_transferencia)
        
        
    else:
        logger.error("No se ha encontrado la tabla. No se puede proceder!")

if __name__ == "__main__":
    
    logger.info('\n\n\n\n\nIniciando aplicación!!\n\n\n\n\n')
    buscar_tabla_lista_personajes()
    buscar_info_personajes()
    