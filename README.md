# DATAMAD 2024

Este es un proyecto realizado para DATAMAD 2024 en el que se utilizan datos de Idealista y datos del Portal de Datos Abiertos de la Comunidad de Madrid para crear una aplicación web. 

Los dos principales archivos del proyecto son:

## 1. DATAMAD.ipynb

En este cuaderno se realiza la extracción de los datos. Por un lado se realiza un scraping a la web de Idealista y por otro se recurre a una API para acceder a los datos de la Comunidad de Madrid. Finalmente, se añaden y normalizan las coordenadas de todos los datasets para que tengan el formato UTM y se permita así el cálculo de distancias. 

## 2. app.py

En este programa se realiza la aplicación web utilizando el paquete streamlit. El programa consiste en visualizar los datasets realizando un cálculo de distancias y permitiendo hacer un filtrado por parámetros comunes de cualquier web de buscar piso y además filtros propios de los datos abiertos de la Comunidad de Madrid. 
