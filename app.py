import pandas as pd
import streamlit as st
import numpy as np

# Función para calcular la distancia entre dos puntos geográficos
def calcular_distancia(lat1, lon1, lat2, lon2):
    try:
        # Convertir grados a radianes
        lat1_rad = np.radians(lat1)
        lon1_rad = np.radians(lon1)
        lat2_rad = np.radians(lat2)
        lon2_rad = np.radians(lon2)

        # Fórmula de Haversine
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        # Radio de la Tierra en metros
        r = 6371000
        return r * c  # Distancia en metros
    except Exception as e:
        st.error(f"Error en el cálculo de distancia: {e}")
        return np.nan

# Cargar la base de datos de pisos y desfibriladores
pisos_df = pd.read_csv(r'G:\Mi unidad\Máster UCM\DATAMAD\DATAMAD\casas_con_coordenadas_transformadas.csv', delimiter=';')
desfibriladores_df = pd.read_csv(r'G:\Mi unidad\Máster UCM\DATAMAD\DATAMAD\desfibriladores.csv', delimiter=';', encoding='latin1')
centros_sanitarios_df = pd.read_csv("datos_madrid_latlon.csv")  # Cargar los centros sanitarios

# Verificar si hay valores NaN en coordenadas
if pisos_df['LATITUD'].isnull().any() or pisos_df['LONGITUD'].isnull().any():
    st.warning("Hay valores NaN en las coordenadas de los pisos. Verifica los datos.")
if centros_sanitarios_df['latitud'].isnull().any() or centros_sanitarios_df['longitud'].isnull().any():
    st.warning("Hay valores NaN en las coordenadas de los centros sanitarios. Verifica los datos.")

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

# Filtro de distancia a desfibriladores
st.sidebar.header("Filtrar por cercanía a desfibriladores")
distancia_max_desfibrilador = st.sidebar.slider("Distancia máxima a desfibriladores (m)", min_value=0, max_value=5000, value=500)

# Calcular la distancia a desfibriladores
if not pisos_filtrados.empty and not desfibriladores_df.empty:
    # Crear una columna para la distancia mínima a cualquier desfibrilador
    pisos_filtrados['distancia_desfibrilador'] = np.inf  # Inicializa con infinito

    # Iterar sobre cada desfibrilador y calcular distancias
    for _, desfibrilador in desfibriladores_df.iterrows():
        # Asegurarse de que las coordenadas son numéricas
        lat_d = float(desfibrilador['direccion_latitud'].replace(',', '.'))
        lon_d = float(desfibrilador['direccion_longitud'].replace(',', '.'))

        # Calcular distancias
        distancias = pisos_filtrados.apply(lambda x: calcular_distancia(x['LATITUD'], x['LONGITUD'], lat_d, lon_d), axis=1)

        # Actualizar la distancia mínima
        pisos_filtrados['distancia_desfibrilador'] = np.minimum(pisos_filtrados['distancia_desfibrilador'], distancias)

    # Filtrar los pisos según la distancia máxima a desfibriladores
    pisos_filtrados = pisos_filtrados[pisos_filtrados['distancia_desfibrilador'] <= distancia_max_desfibrilador]

# Filtro de distancia a centros sanitarios
st.sidebar.header("Filtrar por cercanía a centros sanitarios")
distancia_max_centro = st.sidebar.slider("Distancia máxima a centros sanitarios (m)", min_value=0, max_value=50000, value=500)

# Calcular la distancia a centros sanitarios
if not pisos_filtrados.empty and not centros_sanitarios_df.empty:
    # Crear una columna para la distancia mínima a cualquier centro sanitario
    pisos_filtrados['distancia_centro_sanitario'] = np.inf  # Inicializa con infinito

    # Iterar sobre cada centro sanitario y calcular distancias
    for _, centro in centros_sanitarios_df.iterrows():
        # Asegurarse de que las coordenadas son numéricas
        lat_c = centro['latitud']
        lon_c = centro['longitud']

        # Calcular distancias
        distancias_centros = pisos_filtrados.apply(lambda x: calcular_distancia(x['LATITUD'], x['LONGITUD'], lat_c, lon_c), axis=1)

        # Actualizar la distancia mínima
        pisos_filtrados['distancia_centro_sanitario'] = np.minimum(pisos_filtrados['distancia_centro_sanitario'], distancias_centros)

        # Imprimir las distancias calculadas para depuración
       # for index, distancia in enumerate(distancias_centros):
        #    st.write(f"Distancia desde {pisos_filtrados.iloc[index]['titulo']} a centro sanitario: {distancia:.2f} metros.")

    # Filtrar los pisos según la distancia máxima a centros sanitarios
    pisos_filtrados = pisos_filtrados[pisos_filtrados['distancia_centro_sanitario'] <= distancia_max_centro]

# Mostrar resultados filtrados en la aplicación
st.subheader("Pisos encontrados")
if not pisos_filtrados.empty:
    st.write(pisos_filtrados[['titulo', 'localizacion', 'precio', 'metros_cuadrados', 'distancia_desfibrilador', 'distancia_centro_sanitario']])
else:
    st.warning("No se encontraron pisos que cumplan con los criterios de búsqueda.")
