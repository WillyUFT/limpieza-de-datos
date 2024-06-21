###################
# ! Williams Durán
# ! Limpieza de datos

# ^ Importaciones
import pandas as pd
import requests
from bs4 import BeautifulSoup

def obtener_datos_base(url):
    
    # & Estos son los datos que retornaremos en forma de diccionario
    nombre = ""
    rating = ""
    rareza = ""
    elemento = ""
    tipo_arma = ""
    jp_seiyuu = ""
    en_seiyuu = ""
    
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "lxml")
    
    # ^ Este h3 contiene como el título del character info, por lo que
    # ^ podemos ubicar la tabla de información del personaje con él
    h3_personaje_info = soup.find("h3", string="Character Information")
    
    if h3_personaje_info:
        
        # & Acá extraemos la tabla que contiene los datos base
        tabla_datos = h3_personaje_info.find_next("table", class_ = "a-table")
        
        if tabla_datos:
            
            # & Extraemos el nombre
            fila_nombre = tabla_datos.find_next("tr")
            nombre = fila_nombre.find("th").text.strip()
            
            # & Extraemos el resto de filas
            filas = tabla_datos.find_all("tr")
            
            for fila in filas:
                
                # ^ la tabla está como traspuesta, entonces, el th, que está dentro
                # ^ del tr, contiene el nombre de la información, meientras que el 
                # ^ td contiene la información como tal (ver imágen):
                # ^ imagen tabla_th_td
                th_td = fila.find_all(["th","td"])
                
                if len(th_td) > 1:
                                        
                    # & Extraemos el encabezado
                    encabezado = th_td[0].text.strip()
                                        
                    # & Buscamos el rating
                    
                    # & Hay ocasiones, por lo general para personajes nuevos, que la tabla está uultra
                    # & desordenada, por lo que tenemos que hacer algunos malabares para encontrar el rating
                    
                    # & Así, a veces tenemos tres columnas dentro de la fila, cómo se ve en la imagen
                    # & tres_columnas_rating 
                    if len(th_td) > 2 and 'rowspan' in th_td[0].attrs and th_td[1].text.strip() == "Rating":
                        
                        # & Sacamos el rating
                        icon = th_td[2].find("img")
                        if icon and 'alt' in icon.attrs:
                            rating = icon['alt'].replace(" Rank Icon", "")

                    # & Sacamos el rating para situaciones normales, menos mal!
                    # & rango_alt
                    elif th_td[0].text.strip() == "Rating":
                        icon = th_td[1].find("img")
                        if icon and 'alt' in icon.attrs:
                            rating = icon['alt'].replace(" Rank Icon", "")
                    
                    # & Esta información es solo texto, por lo que es bastante simple de obtener!
                    elif encabezado == "Rarity":
                        rareza = th_td[1].text.strip()
                        
                    elif encabezado == "Element":
                        elemento = th_td[1].text.strip()
                        
                    elif encabezado == "Weapon":
                        tipo_arma = th_td[1].text.strip()
                        
                    elif encabezado == "Voice Actors":
                        
                        # & Cómo las actrices vienen juntas y simplemente están separadas por un
                        # & <br> tendremos que buscar un método un poco más agresivo para obtenerlas
                        # & seiyuu_br
                        actrices = th_td[1].contents
                        
                        for contenido in actrices:
                            
                            # & Formato para personajes más antiguos
                            if isinstance(contenido, str) and "EN Voice Actor" in contenido:
                                en_seiyuu = contenido.replace("EN Voice Actor: ", "").strip()
                            elif isinstance(contenido, str) and "JP Voice Actor" in contenido:
                                jp_seiyuu = contenido.replace("JP Voice Actor: ", "").strip()
                                
                            # & Formato de personajes nuevos
                            elif isinstance(contenido, str) and "(EN)" in contenido:
                                en_seiyuu = contenido.replace("(EN)", "").strip()
                            elif isinstance(contenido, str) and "(JP)" in contenido:
                                jp_seiyuu = contenido.replace("(JP)", "").strip()
                              
    
    diccionario = {
        "nombre": nombre,
        "rating": rating,
        "rareza": rareza,
        "elemento": elemento,
        "tipo_arma": tipo_arma,
        "jp_seiyuu": jp_seiyuu,
        "en_seiyuu": en_seiyuu
    }
    
    print (diccionario)
    return diccionario;
            
# & Traemos el excel en modo pandas
df = pd.read_excel('Genshin_Impact_Characters.xlsx')


# Lista para almacenar los datos de cada personaje
datos_personajes = []

for personaje in range(10):
    
    # ^ Obtenemos los datos del personaje
    nombrePersonaje = df.iloc[personaje]['Name']
    link = df.iloc[personaje]['URLS']
    
    # Buscamos la tabla
    datos_personaje = obtener_datos_base(link)
    
    # Añadimos los datos a la lista
    datos_personajes.append(datos_personaje)
    
# & Creamos el dataframe en el que guardaremos todo
df_final = pd.DataFrame()
columnas = ['Nombre', 'Elemento', 'Rating', 'Tipo de arma', 
            'Rareza', 'Actor de voz EN', 'Actor de voz JP',
            'Main DPS', 'Sub-DPS', 'Support', 'Exploración',
            'Mejor arma', 'Mejor arma F2P', 'Base Hp', 'Base ATK',
            'Base DEF', 'Base HP', 'Base ATK', 'Base DEF']

# Guardamos el DataFrame en un archivo Excel
df_final.to_excel("Genshin_Impact_Characters_Final.xlsx", index=False)
print(df_final)
    
    
        
        
        
        
    
    
    
    
    
    

    

    
    
    
    
    