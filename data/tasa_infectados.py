# #######################################################################################################################################
# Genera la tabla infectadosxdia que contiene la cantidad de infectados y muertes por día, no el total sino los caos nuevos.
# Lo procesa con los países limítrofes (fijo por list) y los top 10 de los paises obtenidos durante la ejecución.
# En cada ejecución la tabla tiene un delete con lo cual se recalculan todos los datos y se ingresan.
# Hernan -  2020-04-10 - Version 1.
# Hernan -  2020-04-21 - Version 2. Optimización de código + Eliminación de tabla covid19_tasa_inf + Agregado de muertes por día.
# #######################################################################################################################################

import psycopg2
from datetime import datetime
import os

vpais_actual = "Argentina"
infxhora = 0
c = 0
lpais = []
linfxdia = []
lmuexdia = []
lfecha = []
valor = 0
ahora = datetime.now()
vfecha = ahora.strftime("%Y-%m-%d %H:%M")

# Agrego Argentina y los paises limitrofes a la consulta.
lpaises = []
lpaises.append("Argentina")
lpaises.append("Brazil")
lpaises.append("Chile")
lpaises.append("Paraguay")
lpaises.append("Bolivia")
lpaises.append("Uruguay")

# Leo las variables para conectarme a Postgresql.
phost = os.environ['hac_PHOST']
puser = os.environ['hac_PUSERNAME']
pdatabase = os.environ['hac_PDATABASE']
ppassword =  os.environ['hac_PPASSWORD']


# Genero la conexion con la base. VARIABLES DE ENTORNO - Hernan 2020-04-21
conn = psycopg2.connect(
    host = phost,
    database = pdatabase,
    user = puser,
    password = ppassword
)

# Genero la conexion con la base. RODRI
#conn = psycopg2.connect(
#    host = "postgresql",
#    database="salud",
#    user="pi",
#    password="Software26"
#)

# Creo el cursor Con los 10 paises que mas infectados tienen.
cur = conn.cursor()

cur.execute("select pais, max(infectados) from covid19 group by pais order by 2 desc limit 10")
rows = cur.fetchall()

# Cargo los paises para el IN para sacar luego la consulta.
for reg in rows:

    lpaises.append(reg[0])


# Creo el cursor Con los paises y sus infectados. Hernan 2020-04-21 Optimizado.
cur = conn.cursor()

cur.execute("select date(fecha) as dia, pais, max(infectados) as infectados,\
  max(muertes) as muertes from covid19 where pais in \
  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
  group by dia, pais \
  order by 2,1", (lpaises))

rows = cur.fetchall()

for reg in rows:


    # Si es el mismo pais.
    if  reg[1] == vpais_actual:

        # Si ES el primer registro del cursor ?
        if c < 1:

            # Si es el primer registro inicializo infxhora con el valor de infectados.
            infxdia = reg[2]
            muexdia = reg[3]
        
        else:

            # Si no es el primero y sigo en el mismo pais infxhora es el actual menos el anterior.
            infxdia = reg[2] - valor_inf
            muexdia = reg[3] - valor_mue


    else:

        # Si cambia el pais inicializo infxdia y muexdia con el actual y la variable de pais actual.

        vpais_actual = reg[1]
        infxdia = reg[2]
        muexdia = reg[3]

    valor_inf = reg[2]
    valor_mue = reg[3]

    # Incremento el contador.
    c = c + 1

    # Cargo los datos en la tabla en memoria si la cantidad es mayor a cero.
    # Así elimino cuando no hubo cambios o si da nergativo por error en la carga de los datos.
    # Hernan 2020-04-21.
    
    if infxdia > 0:
        
        # Obtengo el día de hoy PARA no tener PARCIALES.
        # Guardo en la lista si no es un dato del mismo día.
        # Hernan - 20200412
        
        dia = reg[0]
        dia = datetime.strftime(dia, "%Y-%m-%d")
           
        # Si no es el mismo día de HOY.
        if dia != ahora.strftime("%Y-%m-%d"):
            
            # Y si no es el primer día de la muestra (2020-04-07) para que no empiece con el
            # número total de los casos que es lo que toma al comenzar cada país.
            # Hernan - 20200421
            
            if dia != '2020-04-07':
        
                lfecha.append(reg[0])
                lpais.append(reg[1])
                linfxdia.append(infxdia)
                lmuexdia.append(muexdia)


# Borro todos registros de la tabla infectadosxdia.
cur.execute("delete from infectadosxdia;")

# Cargo la tabla
tt = len(lpais)

for t in range(tt):

    cur.execute("insert into infectadosxdia (dia, pais, infecxdia, muertxdia) \
        values (%s,%s,%s,%s)",\
        (lfecha[t], lpais[t], linfxdia[t], lmuexdia[t]))

# Commit de los inserts.
conn.commit()

# Cierro cursor y conexion.
cur.close()
conn.close()

