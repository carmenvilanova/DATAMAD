import pandas as pd
from scipy.spatial import distance

# Cargar el archivo CSV con los barrios
barrios_df = pd.read_csv('limitesbarrios.csv')

def encontrar_barrio(lat_dada, lon_dado):
    """
    Encuentra el barrio más cercano a las coordenadas dadas.
    
    Args:
    - lat_dada (float): Latitud en UTM.
    - lon_dado (float): Longitud en UTM.
    
    Returns:
    - str: Nombre del barrio más cercano.
    """
    # Crear un array con las coordenadas dadas
    coordenadas_dadas = [lat_dada, lon_dado]
    
    # Inicializar variables para encontrar la distancia mínima
    distancia_minima = float('inf')
    barrio_mas_cercano = None

    # Iterar sobre cada barrio en el DataFrame
    for index, row in barrios_df.iterrows():
        # Crear un array con las coordenadas del barrio
        coordenadas_barrio = [row['Latitude'], row['Longitude']]
        
        # Calcular la distancia
        dist = distance.euclidean(coordenadas_dadas, coordenadas_barrio)
        
        # Si la distancia es menor que la mínima registrada, actualiza
        if dist < distancia_minima:
            distancia_minima = dist
            barrio_mas_cercano = row['Name']
    
    return barrio_mas_cercano

# Ejemplo de uso de la función
latitud = 440953  # Latitud de ejemplo
longitud = 4477003  # Longitud de ejemplo
barrio = encontrar_barrio(latitud, longitud)

# Mostrar el resultado
if barrio:
    print(f'El barrio correspondiente a las coordenadas es: {barrio}')
else:
    print('No se encontró un barrio para las coordenadas proporcionadas.')
