###################
# ! Williams Durán
# ! Limpieza de datos

# ^ Importaciones
import pandas as pd
import requests
from bs4 import BeautifulSoup

def obtener_tabla_personaje(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "lxml")
    
    # ^ Este h3 contiene como el título del character info, por lo que
    # ^ podemos ubicar la tabla de información del personaje con él
    h3_personaje_info = soup.find("h3", string="Character Information")
    
    # ^ Si encontramos el h3
    if h3_personaje_info:
        return h3_personaje_info.find_next("table", class_ = "a-table")
    else:
        return None

# & Traemos el excel en modo pandas
df = pd.read_excel('Genshin_Impact_Characters.xlsx')

for personaje in range(len(df)):
    
    # ^ Obtenemos los datos del personaje
    nombrePersonaje = df.iloc[personaje]['Name']
    link = df.iloc[personaje]['URLS']
    
    # ^ Buscamos la tabla
    tabla_personaje = obtener_tabla_personaje(link)
    
    # ^ Si encontramos tabla
    if tabla_personaje:
        df_personaje = pd.read_html(str(tabla_personaje))[0]
        nombreArchivo = "Información de " + nombrePersonaje + ".xlsx" 
        df_personaje.to_excel(nombreArchivo, index=False)
        print(df_personaje)
    
    
    
    
    
    

    

    
    
    
    
    