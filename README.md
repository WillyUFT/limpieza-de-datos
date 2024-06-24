<!-- & --------------------------- INFO_BASE ---------------------------- -->

# Documentación del código

## Archivo main

El Archivo main, cómo su nombre indica es el archivo principal, que el llama a ejecutar todo el resto.

Este código, va a [Game 8](https://game8.co/), una página que se dedica a exponer información, guías, noticias, trucos, etc. Sobre distintos videojuegos. Para esta actividad, se utilizó su apartado de Genshin Impact, el cual contiene mucho de su contenido en tablas html.

### Función buscar_tabla_lista_personajes()

Esta procede a ir a la [lista de personajes](https://game8.co/games/Genshin-Impact/archives/296707) para extraer la lista de personajes, la cual se ve de la siguiente forma. 

![Lista de personajes](/imagenes/tabla_lista_personajes.png)

Para extraer la información se utiliza la librería *Beutiful soup* y se transforma a un dataframe. Luego la tabla extraída, se recorre fila por fila para extraer la url que nos lleva a la información específica de cada personaje, el enlace se encuentra dentro de la columna del nombre. Una vez extraído el link, se agrega en una columna distinta al dataframe, así acceder a ellos más rápidamente en el futuro.

![Dataframe con link](/imagenes/dataframe_lista_personajes.png)

### Función buscar_info_personajes()

Esta función toma el dataframe creado en la función main y comienza a recorrerlo para vistar los enlaces de cada personaje y extraer la información específica de este. La data se trae en forma de diccionario mediante distintas funciones alojadas en diferentes archivos, una vez se tengan todos los diccionarios, se fusionan en uno, se guarda en una lista, se guarda el progreso en caso de que falle y se continúa con el siguiente personaje hasta que se llega al último.

Ya terminado hasta el último de los personajes, se guarda un dataframe con toda la información en formato Excel.

![Dataframe final](/imagenes/dataframe_final.png)

### Función guardar_progreso()

Esta función toma todo el progreso que se ha realizado en la función buscar_info_personajes() y lo guarda en el archivo_progreso, el cual es un json que se creó al momento de ejecutar la función de la búsqueda de información. Con esta función, se asegura que el programa comenzará desde donde quedó la última vez.

### Función cargar_progreso()

Esta función busca el archivo de progreso que se guardó en la última ejecución de buscar_info_personajes, en caso de que dicho archivo esté vacío, se comenzará todo el proceso de nuevo, por el contrario, si contiene algún tipo de progreso, el progtrama retomará desde el último personaje en el archivo de progreso.

## Archivo info_base

Este archivo, trae toda la información base de los personajes, en ella se encuentran básicamente los mismos datos que en la tabla de la lista de personajes, así como también otros datos que podrían ser relevantes, como su rating en el meta o sus actores de voz.

![Tabla de datos del personaje](/imagenes/tabla_datos_ej.png)

### Función obtener_datos_base()

Esta es la función principal del archivo, trae una la tabla de datos del personaje, esta se encuentra bajo un \<h3\> que contiene el título "**Character information**", si dicho título existe, se busca justo debajo de él la tabla de la información. Luego, se comienzan a extraer los datos con una serie de funciones y los comandos entregados por *Beutiful soup*

El nombre del personaje, dada que es una fila que abarca las dos columnas, se extrae por separado y se guarda en un dataframe aparte, luego, al llegar el diccionario que tiene el resto de datos, se unen y se retorna para la función buscar_info_personajes() del archivo main.

### Función extraer_datos_tabla()

Esta función recorre fila por fila la tabla para extraer todos los datos de esta y retornarlos en forma de diccionario. Dependiendo del header, se guarda la información en una variable u otra.

### Función extraer_rating()

Esta función busca el ícono de el rating y extrae el "alt" de la imagen. Esto a veces funciona de distinta manera dependiendo del personaje, por ejemplo, para personajes nuevos como *Furina* la imagen del personaje está dentro de la fila del rating, dificultando el proceso de extracción.

![Tabla de datos para personajes nuevos](/imagenes/tres_columnas_rating.png)

Mientras que para personajes más antigüos como *Ayaka* la tabla está formada de modo normal

![Tabla de datos para personajes antiguos](/imagenes/tabla_th_td.png)

Por lo que la función tendrá una validación para cualquiera de los dos casos.

### Función extraer_actriz_en y función extraer_actriz_jp

Estas funciones hacen lo mismo, pero para distintos casos, los actores están separados por un \<br\>, por lo que no se puede simplemente extraer el texto de la celda, sino que se debe tratar el texto obtenido para recoger únicamente el dato necesitado.

Tal como ocurre con el rating, los personajes nuevos y antigüos tienen formatos distintos, por lo que esta función también cuenta con validaciones para ambos casos.
