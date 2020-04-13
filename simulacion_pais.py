#!/usr/bin/python3.7

import psycopg2, datetime, sys


vpais_sim = ""
linfectados = []
vinfectados = 0
lmuertes = []
vmuertes = 0
c = 1
vahora = datetime.datetime.now()
vhora = vahora.strftime("%H:%M")


print("Simulacion de avance diario segun avance de otro pais.")
vpais_sim = input ("Con que pais desea simular: ")

# Genero la conexion con la base.
conn = psycopg2.connect(
    host = "localhost",
    database="raspi",
    user="pi",
    password="Software26"
)

# Creo el cursor.
cur = conn.cursor()

cur.execute("select fecha, infectados, muertes from covid19 where pais = %s order by fecha desc", (vpais_sim,) )

rows = cur.fetchall()

num_rows = cur.rowcount

if num_rows < 1:
    print ("No se encontro el pais ",vpais_sim)
    # Cierro el cursor y le coneccion a la base.
    cur.close()
    conn.close()
    sys.exit(1)
    
for reg in rows:

    #print (c)
    #sys.stdout.write("Registro: %d%%   \r" % (c) )
    #sys.stdout.flush()
    
    if c > 1:
        
        linfectados.append(vinfectados - reg[1])
        vinfectados = reg[1]
        
        lmuertes.append(vmuertes - reg[2])
        vmuertes = reg[2]
        
    
    else:
        
        # Si es el primer registro carga el valor en la variable.
        vinfectados = reg[1]
        vmuertes = reg[2]
        
    c = c + 1
    
        
promedio_infectados = int ((sum(linfectados)/len(linfectados)))
promedio_muertes = int((sum(lmuertes)/len(lmuertes)))
    
print ("Promedio de infectados por hora para ",vpais_sim,": ",promedio_infectados)

# Obtengo el ultimo valor de Argentina

cur.execute("select fecha, infectados, muertes from covid19 where pais = 'Argentina' order by fecha desc LIMIT 1")

rows = cur.fetchall()

for reg in rows:
    
    varg_infectados = reg[1]
    varg_muertes = reg[2]

# Simula por las proximas 48 horas.
for hora in range(48):
    #print ("    HORA          INFECTADOS         MUERTES")
    #print ("   ", vhora, "          ",varg_infectados+promedio_infectados, "          ",varg_muertes + promedio_muertes)
    print ("    HORA          INFECTADOS")
    print ("   ", vhora, "          ",varg_infectados+promedio_infectados)

    varg_infectados = varg_infectados+promedio_infectados
    varg_muertes = varg_muertes + promedio_muertes
    vahora = vahora + datetime.timedelta(hours=1)
    vhora = vahora.strftime("%H:%M")

# Cierro el cursor y le coneccion a la base.
cur.close()
conn.close()