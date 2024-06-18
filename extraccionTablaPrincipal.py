###################
# ! Williams Durán
# ! Limpieza de datos

# & Este código va a una página que contiene información sobre el Genshin Impact
# & Luego, extrae la lista de personajes que está dentro de la url, esta es una tabla
# & que contiene el nombre, elemento, arma y rareza del personaje.
# & Cuando extraemos la tabla, recorremos las filas para encontrar el link hacia
# & la información del personaje, lo guardamos en una lista y lo agregamos en una
# & nueva columna del dataframe, para posteriormente exportarlo a un archivo excel.

#^ Importaciones
import pandas as pd
import utiles

# & Obtenemos la URL principal
table_principal = utiles.obtener_tabla("https://game8.co/games/Genshin-Impact/archives/296707",
                                       "a-table a-table a-table flexible-cell")

# & Si la tabla existe
if table_principal:
    # ! Convertimos la tabla HTML en un DataFrame de pandas
    df_principal = pd.read_html(str(table_principal))[0]
    
    # ^ Sacamos los headers de la tabla, para poder sacar los links de cada personaje
    rows = table_principal.find_all("tr")[1:]
    
    # ^ Comenzamos a guardar los links en una lista
    urls = []
    
    # ^ Buscamos en la primera columna el link hacia la información del personaje
    for row in rows:
        first_cell = row.find_all("td")[0]
        link = first_cell.find("a", class_="a-link")
        if link and 'href' in link.attrs:
            urls.append(link['href'])
        else:
            urls.append(None)

    # ^ Agregamos una columna nueva al data frame con los links de cada personaje
    df_principal['URLS'] = urls

    # ^ Guardamos el Excel
    df_principal.to_excel("Genshin_Impact_Characters.xlsx", index=False)
    print(df_principal)
    
else:

    print("Tabla no encontrada.")