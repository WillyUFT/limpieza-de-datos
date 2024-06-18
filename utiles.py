###################
# ! Williams Durán
# ! Limpieza de datos

# & Este archivo almacena distinas funciones que nos serán útiles
# & en mútiples ficheros

#^ Importaciones
import requests
from bs4 import BeautifulSoup

# & Función para obtener tablas de una URL específica
def obtener_tabla(url, clase: str):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "lxml")
    table = soup.find("table", class_ = clase)
    return table
