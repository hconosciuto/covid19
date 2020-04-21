import psycopg2
from datetime import datetime
import os

vpais_actual = "Argentina"
infxhora = 0
c = 1
lpais = []
linfectados = []
linfxhora = []
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

#print (phost)
#print (puser)
#print (pdatabase)
#print (ppassword)

# Genero la conexion con la base. VARIABLES DE ENTORNO - Hernan 2020-04-21
conn = psycopg2.connect(
    host = phost,
    database = pdatabase,
    user = puser,
    password = ppassword
)

# Genero la conexion con la base. HERNAN
#conn = psycopg2.connect(
#    host = "postgresql",
#    database="salud",
#    user="pi",
#    password="Software26"
#)

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


#print (lpaises)

# Creo el cursor Con los paises y sus infectados.
cur = conn.cursor()

cur.execute("select fecha, pais, infectados from covid19 where pais in\
  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
  order by 2,1", (lpaises))

rows = cur.fetchall()

for reg in rows:

    #print (reg[0], reg[1], reg[2])

    if  reg[1] == vpais_actual:

        # Es el primer registro del cursor ?
        if c > 1:

            # Si no es el primero y sigo en el mismo pais infxhora es el actual menos el anterior.
            infxhora = reg[2] - valor

        else:

            # Si es el primer registro inicializo infxhora con el valor de infectados.
            infxhora = reg[2]
            infxhora = 0

    else:

        # Si cambia el pais inicializo infxhora con el actual y la variable de pais actual.

        #print ("Cambio el pais!")
        vpais_actual = reg[1]
        valor = reg[2]
        infxhora = 0

    valor = reg[2]
    # Si la diferencia es cero no se registra

    c = c + 1
    #print (reg[1], reg[2], infxhora)
    #print (c)

    # Cargo los datos en la tabla en memoria si la cantidad no es cero.

    if infxhora != 0:
        
        # Obtengo el día de hoy PARA no grabar el día de hoy ya que el grafico confunde.
        # Guardo en la lista si no es un dato del mismo día.
        # Hernan - 20200412
        
        dia = reg[0]
        dia = datetime.strftime(dia, "%Y-%m-%d")
                        
        if dia != ahora.strftime("%Y-%m-%d"):
        
            lpais.append(reg[1])
            linfectados.append(reg[2])
            linfxhora.append(infxhora)
            lfecha.append(reg[0])


# Inicializo la tabla.
cur.execute("delete from covid19_tasa_inf")
conn.commit()

# Cargo la table
tt = len(lpais)

for t in range(tt):

    #print ("Pais: ", lpais[t]," infectados: ", linfectados[t], " infxhora:", linfxhora[t])

    cur.execute("insert into covid19_tasa_inf (fecha, pais, infectados, infectadosxhora) values (%s,%s,%s,%s)",\
               (lfecha[t], lpais[t], linfectados[t], linfxhora[t]))

conn.commit()

# Borro la tabla de acumulados por dia.
cur.execute("drop table infectadosxdia;")

# Creo la tabla acumulados por dia.
cur.execute("select date(fecha) as dia, pais, sum(infectadosxhora) as infecxdia \
    into infectadosxdia from covid19_tasa_inf group by dia, pais order by 2,1;")

conn.commit()
# Cierro cursor y conexion.
cur.close()
conn.close()

