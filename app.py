import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt



df = pd.read_csv("peliculas.csv")


st.title("Peliculas")

#columnas en español
df = df.rename(columns={
    "Title": "Título",
    "Genre": "Género",
    "Director": "Director",
    "Actors": "Actores",
    "Year": "Año",
    "Runtime (Minutes)": "Duración (Minutos)",
    "Rating": "Calificación",
    "Votes": "Votos",
    "Revenue (Millions)": "Ingresos (Millones)",
    "Metascore": "Puntuación"
})

#tabla con las 10 películas con más ingresos
st.write("Las 10 películas con más ingresos:")
tabla_ingresos = df[["Título", "Director", "Ingresos (Millones)"]].sort_values(by="Ingresos (Millones)", ascending=False).head(10)
st.table(tabla_ingresos)





# relación entre duración y millones en ingresos
relacion_duracion_ingresos = df[["Duración (Minutos)", "Ingresos (Millones)"]].corr(method="pearson").iloc[0, 1]




#gráfico de dispersión con la relación entre calificación y duración
st.write("Relación entre calificación y duración:")
grafico_calificacion_duracion = df.plot(kind="scatter", x="Duración (Minutos)", y="Calificación")
st.pyplot(grafico_calificacion_duracion.get_figure())





# actores que más aparecen
top_actores = df['Actores'].str.split(', ').explode().value_counts().head(10)

# Renombra columnas en español
top_actores = top_actores.rename_axis('Actor').reset_index(name='Apariciones')


st.write("Actores que más aparecen en esta lista:")
st.table(top_actores)




#gráfico de barras con los actores que más aparecen
st.write("Actores que más aparecen en esta lista:")
grafico_actores = alt.Chart(top_actores).mark_bar().encode(
    x="Apariciones",
    y=alt.Y("Actor", sort="-x"),
    color="Apariciones"
)
st.altair_chart(grafico_actores, use_container_width=True)





#gráfico de barras con los géneros más populares
st.write("Géneros más populares:")
generos = df['Género'].str.split(', ').explode().value_counts().reset_index()
grafico_generos = alt.Chart(generos).mark_bar().encode(
    x=alt.X('index:N', axis=alt.Axis(title='Género')),
    y=alt.Y('Género:Q', axis=alt.Axis(title='Número de películas')),
    color=alt.Color('Género:N', legend=None)
)
st.altair_chart(grafico_generos, use_container_width=True)







#gráfico de barras con los directores más populares
st.write("Directores más populares:")
directores = df['Director'].str.split(', ').explode().value_counts().head(10).reset_index()
grafico_directores = alt.Chart(directores).mark_bar().encode(
    x=alt.X('index:N', axis=alt.Axis(title='Director')),
    y=alt.Y('Director:Q', axis=alt.Axis(title='Número de películas')),
    color=alt.Color('Director:N', legend=None)
)
st.altair_chart(grafico_directores, use_container_width=True)



# cantidad de géneros
generos = df['Género'].str.split(', ').explode().value_counts()

# gráfico de pastel
grafico_generos = alt.Chart(generos.reset_index()).mark_arc().encode(
    theta='Género:Q',
    color='index:N',
    tooltip=['index:N', 'Género:Q']
).properties(
    width=500,
    height=500
)


st.write("Distribución de géneros:")
st.altair_chart(grafico_generos, use_container_width=True)



calificacion_promedio_por_anio = df.groupby(df['Año'].astype(int))['Calificación'].mean().reset_index()

calificacion_promedio_por_anio['Año'] = calificacion_promedio_por_anio['Año'].astype(int).astype(str)

grafico_calificacion_promedio = alt.Chart(calificacion_promedio_por_anio).mark_line().encode(
    x='Año',
    y='Calificación',
).properties(
    width=600,
    height=400,
    title='Evolución de la calificación promedio de las películas'
)

st.altair_chart(grafico_calificacion_promedio, use_container_width=True)




# Agrupar las películas por año y encontrar la fila con la calificación más alta para cada grupo
idx = df.groupby('Año')['Calificación'].idxmax()

# filas correspondientes de la tabla original y ordenarlas por año
top_movies = df.loc[idx, ['Título', 'Año', 'Calificación']].sort_values('Año')

#la columna Calificación a 2 decimales
top_movies['Calificación'] = top_movies['Calificación'].apply(lambda x: round(x, 2))

st.write("Película más valorada por cada año:")
st.table(top_movies)





st.write("Géneros menos votados:")
# Calcular la media de votos por género y ordenar de menor a mayor media
media_votos_por_genero = df.groupby('Género')['Votos'].mean().sort_values()

#  5 géneros con la media de votos más baja
generos_menos_votados = media_votos_por_genero.head(5)

st.write(generos_menos_votados)



#lista con todos los directores únicos en el DataFrame
directores = sorted(df['Director'].unique())

#añade selector de director en la interfaz de Streamlit
selected_director = st.selectbox('Seleccione un director', directores)

# Filtrado de el DataFrame según el director seleccionado
df_filtrado = df[df['Director'] == selected_director]

# Obtener una lista de películas dirigidas por el director seleccionado
peliculas = df_filtrado['Título'].tolist()


st.write('Director:', selected_director)
st.table(df_filtrado[['Título', 'Año', 'Género']])




#lista con todos los géneros únicos en el DataFrame
generos = sorted(df['Género'].unique())

#Agrega un selector de género en la interfaz de Streamlit
selected_genero = st.selectbox('Seleccione un género', generos)

#Filtra DataFrame según el género seleccionado
df_filtrado = df[df['Género'] == selected_genero]

#tabla con las películas del género seleccionado
st.table(df_filtrado[['Título', 'Año', 'Director']])





st.write("Películas por género y año: (hay muchas vacías)")

#lista con todos los géneros únicos
generos = sorted(df['Género'].unique())

#selector de género en la interfaz
selected_genero = st.selectbox('Seleccione un género', generos, key='genero_selector')

#lista con todos los años únicos 
anios = sorted(df['Año'].unique())


selected_anio = st.selectbox('Seleccione un año', anios, key='anio_selector')

#Filtra el DataFrame según el género y año seleccionados
df_filtrado = df[(df['Género'] == selected_genero) & (df['Año'] == selected_anio)]


st.table(df_filtrado[['Título', 'Director']])





st.write("¿Qué porcentaje de cada género sale en cada año?")

anios = sorted(df['Año'].unique())

# Agregar un selector de año en la interfaz de Streamlit
selected_anio = st.selectbox('Seleccione un año', anios)

# Filtrar el DataFrame según el año seleccionado
df_filtrado = df[df['Año'] == selected_anio]

# Calcular el porcentaje de películas por género
pct_por_genero = df_filtrado['Género'].value_counts(normalize=True) * 100

# Crear una tabla con los porcentajes de cada género por año
tabla_porc_generos = pd.DataFrame({'Porcentaje': pct_por_genero})
tabla_porc_generos.index.name = 'Género'
tabla_porc_generos = tabla_porc_generos.reset_index()
tabla_porc_generos['Año'] = selected_anio
tabla_porc_generos = tabla_porc_generos[['Género', 'Porcentaje']]
tabla_porc_generos = tabla_porc_generos.sort_values('Porcentaje', ascending=False)

# Mostrar la tabla de porcentajes
st.write("Porcentaje de películas por género en el año seleccionado:")
st.table(tabla_porc_generos)




# Selector de duración máxima en minutos, por defecto en 160 min para que no salga la lista entera
max_dur_min = st.slider('Seleccione la duración mínima a partir de la que le interesan las peliculas:', 0, int(df['Duración (Minutos)'].max()), 160)

#Filtra el DataFrame según la duración máxima seleccionada
df_filtrado = df[df['Duración (Minutos)'] >= max_dur_min]


st.write(f"Películas por duración:")
st.table(df_filtrado[['Título', 'Género', 'Director', 'Duración (Minutos)']])



# Define las opciones de selección del usuario
year_options = sorted(list(df['Año'].unique()))

# Crea un sidebar con el selector de opciones
st.sidebar.title("Elija el año cuyas calificaciones desea ver: (penultima gráfica)")
year = st.sidebar.selectbox("Año", year_options)

# Filtra los datos según el año seleccionado
df_filtered = df[df['Año'] == year]

# Crea el gráfico de barras
bars = alt.Chart(df_filtered).mark_bar().encode(
    x=alt.X('Puntuación:Q', axis=alt.Axis(title='Puntuación')),
    y=alt.Y('Título:N', axis=alt.Axis(title='Película'))
)

# Agregar título al gráfico
title = alt.Chart({'values': [{'text': f"Puntuación de Metacritic para películas de IMDB en {year}"}]}).mark_text(size=20, align='center').encode(text='text:N')

# Muestra el gráfico en la aplicación de Streamlit
st.title(f"Puntuación de Metacritic para películas de IMDB en {year}")
st.altair_chart(bars + title, use_container_width=True)





# Crea un sidebar para que el usuario ingrese manualmente la calificación que desea buscar
st.sidebar.title("Buscar películas por calificación de críticos (saldrá en la última gráfica)")
rating_input = st.sidebar.text_input("Introduce una calificación (de 0.0 a 10.0) es PUNTO, no coma:")

# Convierte la entrada del usuario a un número de punto flotante
try:
    rating = float(rating_input)
except ValueError:
    st.stop()

# Filtra los datos según la calificación introducida por el usuario
filtered_data = df[df['Calificación'] == rating]

# Muestra una tabla con los títulos y directores de las películas con la calificación introducida por el usuario
if not filtered_data.empty:
    st.title("Películas con calificación de " + str(rating))
    st.write(filtered_data[["Título", "Director", "Año"]])
else:
    st.title("No se encontraron películas con calificación " + str(rating))
