import requests
import json

# Función para obtener las coordenadas geográficas de una ciudad usando MapQuest
def obtener_coordenadas(ciudad):
    endpoint = "https://www.mapquestapi.com/geocoding/v1/address"
    params = {
        "key": "Nr94zfuNXain9rduHMwe2iNjVumdDjZj",
        "location": ciudad,
        "country": "CL,AR",  # Limitamos la búsqueda a Chile (CL) y Argentina (AR)
        "language": "es"  # Idioma de la respuesta en español
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        # Obtenemos las coordenadas de la primera ubicación encontrada
        lat = data['results'][0]['locations'][0]['latLng']['lat']
        lng = data['results'][0]['locations'][0]['latLng']['lng']
        return lat, lng
    except Exception as e:
        print(f"Error al obtener coordenadas: {e}")
        return None, None

# Función para calcular la distancia y la duración del viaje usando MapQuest Directions API
def calcular_distancia_y_duracion(origen, destino, medio_transporte):
    endpoint = "https://www.mapquestapi.com/directions/v2/route"
    params = {
        "key": "Nr94zfuNXain9rduHMwe2iNjVumdDjZj",
        "from": origen,
        "to": destino,
        "routeType": "Avion",  # Tipo de ruta más rápida
        "locale": "es",  # Idioma de la respuesta en español
        "unit": "k"  # Unidades métricas (kilómetros)
    }

    if medio_transporte:
        params["routeType"] = medio_transporte
    
    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        # Extraemos la distancia en kilómetros y millas
        distancia_km = data['route']['distance'] * 1.60934  # Convertimos millas a kilómetros
        distancia_millas = data['route']['distance']
        # Extraemos la duración del viaje
        duracion = data['route']['formattedTime']
        return distancia_millas, distancia_km, duracion
    except Exception as e:
        print(f"Error al calcular distancia y duración: {e}")
        return None, None, None

# Función para mostrar la narrativa del viaje
def narrativa_del_viaje(origen, destino, distancia_millas, distancia_km, duracion, medio_transporte):
    print(f"Viajando desde {origen} hasta {destino}:")
    print(f"Distancia: {distancia_millas:.2f} millas / {distancia_km:.2f} kilómetros.")
    print(f"Duración del viaje ({medio_transporte}): {duracion}.")

# Función principal
def main():
    print("Bienvenido al calculador de distancia y duración de viaje con MapQuest.")
    print("Ingrese 's' en cualquier momento para salir.")
    
    while True:
        origen = input("Ingrese la ciudad de origen (Chile): ")
        if origen.lower() == 's':
            break
        
        destino = input("Ingrese la ciudad de destino (Argentina): ")
        if destino.lower() == 's':
            break
        
        medio_transporte = input("Elija el medio de transporte (Auto, Avion, Micro): ")
        if medio_transporte.lower() == 's':
            break
        
        # Obtener coordenadas de origen y destino
        lat_origen, lng_origen = obtener_coordenadas(origen)
        lat_destino, lng_destino = obtener_coordenadas(destino)
        
        if lat_origen and lng_origen and lat_destino and lng_destino:
            # Calcular distancia y duración del viaje
            distancia_millas, distancia_km, duracion = calcular_distancia_y_duracion(f"{lat_origen},{lng_origen}", f"{lat_destino},{lng_destino}", medio_transporte)
            
            if distancia_millas is not None and distancia_km is not None and duracion is not None:
                # Mostrar la narrativa del viaje
                narrativa_del_viaje(origen, destino, distancia_millas, distancia_km, duracion, medio_transporte)
            else:
                print("Hubo un problema al calcular la distancia y la duración del viaje.")
        else:
            print("Hubo un problema al obtener las coordenadas de origen y destino.")
    
    print("Gracias por usar nuestro servicio.")

if __name__ == "__main__":
    main()





    


