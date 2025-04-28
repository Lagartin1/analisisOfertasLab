#!/bin/bash

# Nombre del archivo .env
archivo_env=".env"

# Verificar si el archivo .env ya existe
if [ -f "$archivo_env" ]; then
    echo "El archivo $archivo_env ya existe. ¿Deseas sobrescribirlo? (s/n)"
    read respuesta
    if [ "$respuesta" != "s" ]; then
        echo "El archivo no ha sido sobrescrito."
        exit 1
    fi
fi

# Crear el archivo .env con variables básicas

echo "Creando el archivo .env..."

cat <<EOL > "$archivo_env"
# Archivo de configuración

LINK_FILE_1=
CSV_CHILETRABAJOS=
CSV_COMPUTRABAJO=
LINK_FILE_2=
CSV_INDEED=
LINK_FILE_3=
GEOPANDAS_JSON=

EOL

echo "El archivo .env ha sido creado exitosamente."
