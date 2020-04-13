import psycopg2, datetime, sys
from decimal import Decimal

#Definicion de Variables
poblacion_argentina = 44270000
vfecha_desde = '2020-04-07'
lfecha = []
linfxmillon = [] # Infectados por millon.
lpinfxmillon = [] # Porcentaje de infectados x millon.


print("Simulacion de avance diario segun avance de otro pais.")
vpais_sim = input ("Con que pais desea simular: ")
 
vfecha_desde = input("Ingrese desde que fecha desea tomar los datos de "+vpais_sim+" ("+vfecha_desde+") :") 

# Genero la conexion con la base.
conn = psycopg2.connect(
    host = "localhost",
    database="raspi",
    user="pi",
    password="Software26"
)

# Creo el cursor.
cur = conn.cursor()


cur.execute("select date(fecha), pais, max(inf_por_millon) from covid19 where pais = %s group by date(fecha),pais",\
           (vpais_sim,) )

rows = cur.fetchall()

num_rows = cur.rowcount

if num_rows < 1:
    print ("No se encontro el pais ",vpais_sim)
    # Cierro el cursor y le coneccion a la base.
    cur.close()
    conn.close()
    sys.exit(1)
    
for reg in rows:
    
    # Cargo los arreglos.
    lfecha.append(reg[0])
    linfxmillon.append(reg[2])
    vporcentaje=reg[2]
    vporcentaje = (vporcentaje/1000000)*100
    lpinfxmillon.append(vporcentaje)


longi=len(lfecha)

for i in range(longi):
    
    print ("Pais seleccionado para simular: ",vpais_sim)
    print ("Muestra obtenida de la fecha  : ", lfecha[i])
    print ("Cantidad infectados por millon: ", linfxmillon[i])  
    print ("porcentaje de inf. por millon: ", lpinfxmillon[i])   

# Obtengo el ultimo valor de Argentina

cur.execute("select date(fecha), pais, max(inf_por_millon) from covid19\
    where pais = 'Argentina' group by date(fecha),pais\
    order by 1 desc limit 1")

rows = cur.fetchall()

for reg in rows:

    varg_fechamuestra = reg[0]
    varg_infxmillon = reg[2]
    #varg_muertes = reg[2]

# Obtengo la cantidad de infectados aprox. segun infxmillon.
varg_infectados = int(round(((poblacion_argentina*varg_infxmillon)/1000000),0))

print (varg_infectados)

print ("     DIA                  INFECTADOS     MUERTES")
 
#print (varg_fechamuestra + datetime.timedelta(days=1))

# Muestro el último valor de Argentina que es donde parto y luego sumo.
longi=len(lfecha)
vfecha_arg = varg_fechamuestra

# Simula por los proximos i días.
for i in range(longi):
    
    #print (varg_fechamuestra, "       ",round(varg_infectados,2), "          ",round(varg_muertes,2))
    print (vfecha_arg, "       ",varg_infectados)

    varg_infectados = int(round(((poblacion_argentina*linfxmillon[i])/1000000),0))
    
    vfecha_arg = vfecha_arg + datetime.timedelta(days=1)
        
# Cierro el cursor y le coneccion a la base.
cur.close()
conn.close()