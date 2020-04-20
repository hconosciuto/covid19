import psycopg2, datetime
import matplotlib.pyplot as plt

left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

lpaises = []
lpaises.append("Argentina")

lpais = []
linfectados = []

# Genero la conexion con la base.
conn = psycopg2.connect(
    host = "postgresql",
    database="salud",
    user="pi",
    password="Software26"
)

# Creo el cursor Con los 10 paises que mas infectados tienen.
cur = conn.cursor()

cur.execute("select pais, max(infectados) from covid19 group by pais order by 2 desc limit 10")
rows = cur.fetchall()

for reg in rows:

        lpais.append(reg[0])
        linfectados.append(reg[1])

# Inicializo la tabla covid19_paises_top
cur.execute("delete from covid19_paises_top")
conn.commit()

# Cargo el cursor en la tabla covid_paises_top

for i in range(10):
    cur.execute("insert into covid19_paises_top (pais, infectados) values (%s, %s)", (lpais[i], linfectados[i]))
    conn.commit()


# Cierro el cursor y le coneccion a la base.
cur.close()
conn.close()

# plotting the points
#plt.plot(lpais,linfectados)

plt.bar(left, linfectados, tick_label=lpais,
        width=0.8, color=['red', 'green'])

# naming the x axis
plt.xlabel('PAIS')
# naming the y axis
plt.ylabel('INFECTADOS')

# giving a title to my graph
plt.title('Los 10 paises con mas infectados')

# function to show the plot
plt.show()

