import pandas as pd
import streamlit as st
import numpy as np



# Función para calcular la distancia entre dos puntos geográficos usando la fórmula de Haversine
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

# Cargar las bases de datos
pisos_df = pd.read_csv(r'G:\Mi unidad\Máster UCM\DATAMAD\DATAMAD\casas_con_coordenadas_transformadas.csv', delimiter=';')
desfibriladores_df = pd.read_csv(r'G:\Mi unidad\Máster UCM\DATAMAD\DATAMAD\desfibriladores.csv', delimiter=';', encoding='latin1')
centros_sanitarios_df = pd.read_csv("datos_madrid_latlon.csv")

# Verificar si hay valores NaN en coordenadas
if pisos_df['LATITUD'].isnull().any() or pisos_df['LONGITUD'].isnull().any():
    st.warning("Hay valores NaN en las coordenadas de los pisos. Verifica los datos.")


# Títulos y descripción en Streamlit
st.title("Buscador de Pisos en Madrid")
st.markdown("Filtra pisos utilizando datos abiertos de la Comunidad de Madrid!")

# Filtros de precio y tamaño
st.sidebar.header("Filtros de búsqueda")
precio_min = st.sidebar.number_input("Precio mínimo (€)", min_value=0, value=100000)
precio_max = st.sidebar.number_input("Precio máximo (€)", min_value=0, value=5000000)
tamano_min = st.sidebar.number_input("Tamaño mínimo (m²)", min_value=0, value=10)
tamano_max = st.sidebar.number_input("Tamaño máximo (m²)", min_value=0, value=2000)

# Filtrar pisos por criterios de precio y tamaño
pisos_filtrados = pisos_df[
    (pisos_df['precio'] >= precio_min) &
    (pisos_df['precio'] <= precio_max) &
    (pisos_df['metros_cuadrados'] >= tamano_min) &
    (pisos_df['metros_cuadrados'] <= tamano_max)
]

# Filtro de distancia a desfibriladores
st.sidebar.header("Filtrar por cercanía a desfibriladores")
distancia_max_desfibrilador = st.sidebar.slider("Distancia máxima a desfibriladores (m)", min_value=0, max_value=500, value=100)

if not pisos_filtrados.empty and not desfibriladores_df.empty:
    # Crear columna de distancia mínima a desfibriladores
    distancias_desfibriladores = []
    for _, desfibrilador in desfibriladores_df.iterrows():
        lat_d = float(desfibrilador['direccion_latitud'].replace(',', '.'))
        lon_d = float(desfibrilador['direccion_longitud'].replace(',', '.'))
        distancias = pisos_filtrados.apply(lambda x: calcular_distancia(x['LATITUD'], x['LONGITUD'], lat_d, lon_d), axis=1)
        distancias_desfibriladores.append(distancias)
    # Tomar el mínimo de todas las distancias calculadas para cada piso
    pisos_filtrados['distancia_desfibrilador'] = pd.concat(distancias_desfibriladores, axis=1).min(axis=1)

    # Filtrar por distancia máxima a desfibriladores
    pisos_filtrados = pisos_filtrados[pisos_filtrados['distancia_desfibrilador'] <= distancia_max_desfibrilador]

# Filtro de distancia a centros sanitarios
st.sidebar.header("Filtrar por cercanía a centros sanitarios")
distancia_max_centro = st.sidebar.slider("Distancia máxima a centros sanitarios (m)", min_value=0, max_value=500, value=100)

if not pisos_filtrados.empty and not centros_sanitarios_df.empty:
    # Crear columnas para la distancia mínima y el centro más cercano
    pisos_filtrados['distancia_centro_sanitario'] = np.inf
    pisos_filtrados['centro_sanitario_mas_cercano'] = ""

    for _, centro in centros_sanitarios_df.iterrows():
        lat_c = centro['latitud']
        lon_c = centro['longitud']
        nombre_centro = centro['centro_nro_registro']  # Nombre o identificación del centro

        # Calcular las distancias
        distancias = pisos_filtrados.apply(lambda x: calcular_distancia(x['LATITUD'], x['LONGITUD'], lat_c, lon_c), axis=1)

        # Identificar y actualizar el centro más cercano para cada piso
        is_closer = distancias < pisos_filtrados['distancia_centro_sanitario']
        pisos_filtrados.loc[is_closer, 'distancia_centro_sanitario'] = distancias[is_closer]
        pisos_filtrados.loc[is_closer, 'centro_sanitario_mas_cercano'] = nombre_centro

    # Filtrar por distancia máxima a centros sanitarios
    pisos_filtrados = pisos_filtrados[pisos_filtrados['distancia_centro_sanitario'] <= distancia_max_centro]

# Muestra los resultados de pisos filtrados en un dataframe ajustado
st.subheader("Pisos encontrados")
if not pisos_filtrados.empty:
    st.dataframe(pisos_filtrados[['titulo', 'localizacion', 'precio', 'metros_cuadrados', 'distancia_desfibrilador', 'distancia_centro_sanitario', 'centro_sanitario_mas_cercano']])
else:
    st.warning("No se encontraron pisos que cumplan con los criterios de búsqueda.")

