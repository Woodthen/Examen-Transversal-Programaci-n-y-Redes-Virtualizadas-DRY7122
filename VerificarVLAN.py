#Función para verificar el rango de VLAN

def verificar_vlan(numero_vlan):
    numero_vlan = int(numero_vlan)  # Convertir a entero

    if 1 <= numero_vlan <= 1000:
        return "Normal"
    elif 1002 <= numero_vlan <= 4094:
        return "Extendido"
    else:
        return "Fuera de rango"

numero_vlan = input("Ingrese el número de VLAN: ")
resultado = verificar_vlan(numero_vlan)
print(f"La VLAN {numero_vlan} es del rango {resultado}.")

