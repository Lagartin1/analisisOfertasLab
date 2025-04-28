#  Análisis de Ofertas Laborales en Chile
## Descripción
Este proyecto tiene como objetivo analizar ofertas laborales en Chile utilizando datos extraídos de diferentes plataformas de empleo. Se utilizan técnicas de web scraping para obtener información relevante sobre las ofertas laborales y se realiza un análisis exploratorio de los datos para obtener insights valiosos.

El analisis se realiza en un Jupyter Notebook, donde se presenta el procesamiento de los datos junto a los resultados de manera visual, este notebook se encuentra en la carpeta `src` y el notebook es `AnalisisOfertasLaborales.ipynb`.


## Requisitos previos

1. **Python**: Asegúrate de tener Python instalado en tu sistema.
2. **Liberias de Python**: Este proyecto utiliza varias librerías de Python. Puedes instalar todas las dependencias necesarias utilizando el archivo `requirements.txt` que se incluye en el repositorio, y ejecutando el siguiente comando:
    ```bash
    pip install -r requirements.txt
    ```
3. **Archivo `.env`**: Crea un archivo `.env`, si quieres crear el .env junto con solo los nombres de las variables,ejecuta: 
    ```bash
        chmod +x config.sh
        source ./config.sh
        ```
4. **Variables de entorno**, estas deben ser configuradas con:
   
    | Variable       | Valor            |
    |----------------|------------------|
    | LINK_FILE_1    | ruta a el archivo `links_chiletrabajos.txt`, que contendra links de chiletrabajos(solo usado para scraping)  |
    | CSV_CHILETRABAJOS | ruta a el archivo `csv_chiletrabajos.csv`, que contendra los datos de chiletrabajos , esto esta en la caperta `scrips/data/chiletrabajos` |
    | CSV_COMPUTRABAJO | ruta a el archivo `csv_computrabajo.csv`, que contendra los datos de computrabajo , esto esta en la caperta `scrips/data/computrabajo |
    | CSV_INDEED     | ruta a el archivo `csv_indeed.csv`, que contendra los datos de indeed , esto esta en la caperta `scrips/data/indeed` |
    | LINK_FILE_2    | ruta a el archivo `links_computrabajo.txt`, que contendra links de computrabajo (solo usadas para scraping) |
    | LINK_FILE_3    | ruta a el archivo `links_indeed.txt`, que contendra links de indeed (solo usadas para scraping) |
    | LINK_FILE_4    | ruta a el archivo `.txt`, que contendra links de bumeran (solo usadas para scraping) |
    |GEOPANDAS_JSON| ruta a el archivo `chile.json`, que contendra los datos de geolocalizacion de las regiones de chile, esto esta en la caperta `scrips/data/geopandas` |


## Instrucciones

1. Clona este repositorio:
    ```bash
    git clone https://github.com/Lagartin1/analisisOfertasLab.git
    cd analisisOfertasLab
    ```

2. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

3. Inicia el servidor de Jupyter Notebook:
    ```bash
    jupyter notebook
    ```

4. Abre el archivo `.ipynb` en el navegador y sigue las instrucciones dentro del notebook.

## Notas
- Dentro de la carpeta `scripts` se encuentran los scripts que se utilizan para la el crawling y scraping de los , junto con los datos extraidos.
- Dentro del directorio `/scripts/data` se encuentran los archivos CSV generados por los scripts de scraping.
- Asegúrate de que las variables de entorno en el archivo `.env` estén correctamente configuradas antes de ejecutar el notebook.
- Este proyecto está diseñado para ser ejecutado en un entorno local.

