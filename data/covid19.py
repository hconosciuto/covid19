#!/usr/bin/python3.7

import pandas as pd
import psycopg2
from datetime import datetime
import math

# Obtengo la fecha y hora
# current date and time
ahora = datetime.now()
vfecha = ahora.strftime("%Y-%m-%d %H:%M")

# Leo la pagina y lo mando a dfs
dfs = pd.read_html('https://epidemic-stats.com/coronavirus', header=0)

# Creo un DataFrame desde dfs
df = dfs[0]

# Genero la conexion con la base. HERNAN
conn = psycopg2.connect(
    host = "localhost",
    database="raspi",
    user="pi",
    password="Software26"
)

# Genero la conexion con la base. RODRI
#conn = psycopg2.connect(
#    host = "postgresql",
#    database="salud",
#    user="pi",
#    password="Software26"

# Creo el cursor.
cur = conn.cursor()

# Recorro el Dataframe y cargo los valores en la tabla covid19.
for index, row in df.iterrows():
    vpais = row['Country']
    vinfectados = row['Infected']
    vmuertes = row['Deaths']
    vrecuperados = row['Recovered']
    vporcentaje_muertes = row['Deaths Percent']
    vporcentaje_recuperados = row['Recovered Percent']
    vinf_por_millon = row['Infected per million']
    vmue_por_millon = row['Deaths per million']

    # Muestro el pais que se carga.
    #print("Cargando el pais: ", vpais)

    # Si un valor es NAN lo arreglo para que falle.
    if math.isnan(vmue_por_millon):
       vmue_por_millon = float('0')

    if math.isnan(vinf_por_millon):
       vinf_por_millon = float('0')

    # Quito el signo %.
    vporcentaje_muertes = vporcentaje_muertes[:-1]
    vporcentaje_recuperados = vporcentaje_recuperados[:-1]

    # Convierto los porcentajes en numeros tipo float.
    vporcentaje_muertes = float(vporcentaje_muertes)
    vporcentaje_recuperados = float(vporcentaje_recuperados)

    # Valido que los campos no esten vacios.
    vinf_por_millon = int(vinf_por_millon)
    vmue_por_millon = int(vmue_por_millon)


    # Hago el insert del pais.
    cur.execute("insert into covid19 (fecha, pais, infectados, muertes, recuperados, porcentaje_muertes, porcentaje_recuperados,\
        inf_por_millon, mue_por_millon)\
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (vfecha,vpais, vinfectados, vmuertes, vrecuperados, vporcentaje_muertes,\
            vporcentaje_recuperados, vinf_por_millon, vmue_por_millon) )

# Hago commit. Cierro el cursos y cierro la conexion.
conn.commit()

cur.close()

conn.close()

