import pandas as pd
import streamlit as st

# Cargar la base de datos de pisos
pisos_df = pd.read_csv('G:\Mi unidad\Máster UCM\DATAMAD\DATAMAD\casas_completo.csv', delimiter=';')  # Cambia esta ruta si es necesario

# Títulos y descripción en Streamlit
st.title("Buscador de Pisos en Madrid")
st.markdown("Filtra pisos por criterios de tamaño y precio para encontrar el que mejor se adapte a tus necesidades.")

# Filtros de precio y tamaño
st.sidebar.header("Filtros de búsqueda")

# Precio mínimo y máximo
precio_min = st.sidebar.number_input("Precio mínimo (€)", min_value=0, value=500)
precio_max = st.sidebar.number_input("Precio máximo (€)", min_value=0, value=2000000000)
# Tamaño mínimo y máximo
tamano_min = st.sidebar.number_input("Tamaño mínimo (m²)", min_value=0, value=50)
tamano_max = st.sidebar.number_input("Tamaño máximo (m²)", min_value=0, value=1000000)

# Filtrar pisos por los criterios de precio y tamaño
pisos_filtrados = pisos_df[
    (pisos_df['precio'] >= precio_min) &
    (pisos_df['precio'] <= precio_max) &
    (pisos_df['metros_cuadrados'] >= tamano_min) &
    (pisos_df['metros_cuadrados'] <= tamano_max)
]
# Mostrar resultados filtrados en la aplicación
st.subheader("Pisos encontrados")
st.write(pisos_filtrados[['titulo', 'localizacion', 'precio', 'metros_cuadrados']])
