# Documentación del código

## Archivo main

El Archivo main, cómo su nombre indica es el archivo principal, que el llama a ejecutar todo el resto.

Este código, va a [Game 8](https://game8.co/), una página que se dedica a exponer información, guías, noticias, trucos, etc. Sobre distintos videojuegos. Para esta actividad, se utilizó su apartado de Genshin Impact, el cual contiene mucho de su contenido en tablas html.

### Función buscar_tabla_lista_personajes()

Esta procede a ir a la [lista de personajes](https://game8.co/games/Genshin-Impact/archives/296707) para extraer la lista de personajes, la cual se ve de la siguiente forma.

![Lista de personajes](/imagenes/tabla_lista_personajes.png)

Para extraer la información se utiliza la librería _Beutiful soup_ y se transforma a un dataframe. Luego la tabla extraída, se recorre fila por fila para extraer la url que nos lleva a la información específica de cada personaje, el enlace se encuentra dentro de la columna del nombre. Una vez extraído el link, se agrega en una columna distinta al dataframe, así acceder a ellos más rápidamente en el futuro.

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

Esta es la función principal del archivo, trae una la tabla de datos del personaje, esta se encuentra bajo un \<h3> que contiene el título "**Character information**", si dicho título existe, se busca justo debajo de él la tabla de la información. Luego, se comienzan a extraer los datos con una serie de funciones y los comandos entregados por _Beutiful soup_

El nombre del personaje, dada que es una fila que abarca las dos columnas, se extrae por separado y se guarda en un dataframe aparte, luego, al llegar el diccionario que tiene el resto de datos, se unen y se retorna para la función buscar_info_personajes() del archivo main.

### Función extraer_datos_tabla()

Esta función recorre fila por fila la tabla para extraer todos los datos de esta y retornarlos en forma de diccionario. Dependiendo del header, se guarda la información en una variable u otra.

### Función extraer_rating()

Esta función busca el ícono de el rating y extrae el "alt" de la imagen. Esto a veces funciona de distinta manera dependiendo del personaje, por ejemplo, para personajes nuevos como _Furina_ la imagen del personaje está dentro de la fila del rating, dificultando el proceso de extracción.

![Tabla de datos para personajes nuevos](/imagenes/tres_columnas_rating.png)

Mientras que para personajes más antigüos como _Ayaka_ la tabla está formada de modo normal

![Tabla de datos para personajes antiguos](/imagenes/tabla_th_td.png)

Por lo que la función tendrá una validación para cualquiera de los dos casos.

### Función extraer_actriz_en y función extraer_actriz_jp

Estas funciones hacen lo mismo, pero para distintos casos, los actores están separados por un \<br>, por lo que no se puede simplemente extraer el texto de la celda, sino que se debe tratar el texto obtenido para recoger únicamente el dato necesitado.

Tal como ocurre con el rating, los personajes nuevos y antigüos tienen formatos distintos, por lo que esta función también cuenta con validaciones para ambos casos.

![Fila de las seiyuu](/imagenes/seiyuu_br.png)

## Archivo ranking_por_tipo

Este archivo busca en la tabla de **Tier List Rankig** el desempeño de los personajes en diferentes apartados del juego. Cada personaje es rankeado en cuatro áreas distintas, **Main DPS**, que sería el personaje como fuente de daño principal, **Sub-DPS**, para la fuente secundaria de daño, **Support**, para el personaje como apoyo al resto del equipo y **Exploration** para desplazarse a lo largo del territorio.

![Tabla de datos rating para los personajes](/imagenes/tabla_tier_list_ej.png)

### Función obtener_tabla_list_ranking()

Esta es la función principal, funciona muy similar a otras de este estilo, va a buscar un \<h4> con el título **Tier List Rankings**, para localizar la ubicación de la tabla, y así, obtenerla.

### Función extraer_datos_tabla()

La tabla de rankings es más fácil de leer, pues en primer lugar, no está traspuesta, y el formato no cambia para ningún personaje, por lo que simplemente se lee la fila que contiene las notas de izquierda a derecha, donde **Main DPS** siempre será primero y **Exploration** siempre será último. A medida que se recorren las columnas en la fila, se van asignando los valores a las variables de cada tipo, para posteriormente ser retornadas en forma de diccionario.

![Foramto de la tabla de datos rating para los personajes](/imagenes/tabla_tier_list_formato.png)

### Función extraer_rating()

Esta función toma el \<td> que se el envía, y revisa si es que en dicho tag se encuentra un \<img>, en caso de que exista, retorna el 'alt' de la imagen, que es el que indica el rating en texto, en caso contrario, se retorna un '-', pues no existe información al respecto.

## Archivo stats_personaje

Este archivo contiene las funciones necesarias para extraer las estadísticas base y máximas del personaje a medida que sube de nivel. Estas estadísticas están en dos tablas distintas, pero una está visible, mientras que la otra está oculta. Por lo que se busca la manera de obtener ambas informaciones.

![Tabla de stats para los personajes](/imagenes/tabla_stats_ej.png)

### Función obtener_tabla_stats()

La obtención de información para estas tablas tiene bastantes más dificultades, la primera, el título de la tabla contiene el nombre del personaje, si bien, ya se había tenido un caso similar, en esa parte se tenía un título más o menos largo como para buscarlo con seguridad, acá solo se podría buscar por la palabra _Stats_, lo cual no garantiza traer el \<h3> deseado, por lo que se utilizará una expresión regular para encontrar el encabezado.

Posteriormente, se tiene el problema de la tabla visible y la oculta. Por defecto, la tabla de valores base viene visible, pues el tab que dice _Lvl. 20 Base Stats_ está activado, estos tabs al presionarlos, cambian la clase de las tablas, dependiendo del tab que se presione, la clase pasará a tener _is-active_ y se mostrará. Por lo que para extraer los datos, aprovechando que por defecto viene las stats base activas, se busca esta tabla utilizando la clase _is-active_, mientras que la tabla que viene sí o sí será la de valores máximos.

![Tabla de stats para los personajes](/imagenes/tabla_stats_formato.png)

### Función obtener_stats()

Esta función toma el \<div> de la tabla que quiere analizarse, para posteriormente recorrer fila por fila, obtener los datos y luego retornarlos como diccionario.

## Configuración de Logs

Todos los archivos de código Python contienen una configuración de logs justo debajo de las importaciones, esto se hace con el propósito de obtener información de todo el proceso de extracción de datos.

La configuración está hecha para que, los logs se guerden en un archivo llamado "_Logs.log_", en donde cada línea que se registre contiene la fecha y hora en la que se realizó una operación, el tipo de mensaje que entrega, los **INFO** son enviados por los logs que hay en el código, mientras que los **DEBUG** son emitidos por _Beautiful Soup_, y finalmente, se detalla el mensaje que se busca informar.

![Configuración de logs](/imagenes/logs_config.png)

## Cálculo de costos en tiempo y espacio

En el archivo main, las dos funciones que se encargan de recopilar la información cuentan con un cálculo de tiempo y espacio en el computador.

Para la función buscar_tabla_lista_personajes, se calcula el tiempo y espacio total utilizado para extraer los datos de la tabla que contiene la lista de personajes

![Cálcuo de costos por personaje](/imagenes/calculo_costo_lista_personajes.png)

Para la función buscar_info_personajes() se realiza un cálculo de tiempo y espacio por cada personaje, así como el costo total del proceso

![Cálcuo de costos por personaje](/imagenes/calculo_costos_personajes.png)
