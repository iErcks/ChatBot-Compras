import json
import re

# Cargar el archivo JSON
with open('c:\\Users\\erick\\OneDrive\\Documentos\\ISC\\Semestre7\\MachineLearning\\ChatBot\\SoporteAyuda.json', 'r', encoding='utf-8') as file:
    mybd = json.load(file)

# Filtrar y obtener los datos del JSON de soporte
datos = {}  # Diccionario con toda la base de datos del JSON

# Guardar todo el JSON en un diccionario
for expresion in mybd:
    datos[expresion['id']] = {
        'nombre': expresion['nombre'],
        'Expresion': expresion['Expresion'],
        'Respuesta': expresion['Respuesta']
    }


DiccID = {}

DiccID = {
    'Seguimiento': 3
}

EstadoSig = 0
EstadoAnt = 0

def inputRespuesta():
    opcion = input("Explica tu asunto: ")
    return opcion
    #YesID: Meterte dentro del arbol. noID: Siguiente categoria dentro del mismo nivel

def buscarCoincidencia(opcion, noID):
    global categoria_id
    global EstadoSig
    global EstadoAnt
    expresionesID = {k: v for k, v in datos.items() if k.startswith(categoria_id)}
    for key, coincidencia in expresionesID.items():  # Corrección aquí
        if re.search(coincidencia['Expresion'], opcion):
            print(f"Tu asunto es -{coincidencia['nombre']}- te dirigiremos al area correspondiente")
            EstadoAnt = EstadoSig
            EstadoSig = DiccID[coincidencia['nombre']]
            print (EstadoSig)
            return True
    categoria_id = noID
    return False


expresionesID = {}
categoria_id = '1'

salida = True

##Agregar solo minisculas

categoriasP= ['1', '2']
categoriasH = ['1.1', '1.2', '1.3']
print("Bienvenido a nuestro chatbot")

opcion = inputRespuesta()
for n in categoriasP:
    if buscarCoincidencia(opcion, n):
        break



while salida:
    if EstadoSig == 0: #Estado inicial '1'
        categoria_id = '1'
        opcion = inputRespuesta()
        if buscarCoincidencia(opcion, '2'): #Soporte y ayuda     

            continue
        elif buscarCoincidencia(opcion, '0'): #Compras
            EstadoAnt = EstadoSig
            EstadoSig = 22222222 #Cambiar con categoriaID = '2.1'
            continue
        else:  #No encontro coincidencia
            print("¿Puedes reformular tu pregunta?")
    if EstadoSig == 1: #Soporte y ayuda
        categoria_id = '1.1'
        opcion = inputRespuesta()
        if buscarCoincidencia(opcion, '1.2'): # Pedidos
            EstadoAnt = EstadoSig
            EstadoSig = 2
            continue
        elif buscarCoincidencia(opcion,'1.3'): #Añadir reseña 
            EstadoAnt = EstadoSig
            EstadoSig = 33333333 # categoria id = '1.2.1'
            continue
    if EstadoSig == 2: # Soporte/Pedidos '1.1.1'
        categoria_id = '1.1.1'
        opcion = inputRespuesta()
        if buscarCoincidencia(opcion,'1.1.2'): # Seguimiento
            EstadoAnt = EstadoSig
            EstadoSig = 3
        elif buscarCoincidencia(opcion, '1.1.3'): # Problemas con el pedido
            EstadoAnt = EstadoSig
            EstadoSig = 4
            continue
        elif buscarCoincidencia(opcion, '1.1.4'): # cancelar pedido 
            EstadoAnt = EstadoSig
            EstadoSig = 6
            continue
        elif buscarCoincidencia(opcion, '0'): # Modificar direccion
            EstadoAnt = EstadoSig
            EstadoSig = 7
            
        else:
            print ("¿Puede reformular su pregunta? ----")
    if EstadoSig == 3: # Soporte/Pedidos/Seguimiento '1.1.1.1'
        categoria_id = '1.1.1.1'
        opcion = inputRespuesta()
        if buscarCoincidencia(opcion,'1.1.1.2'): # Rastreo
            EstadoAnt = EstadoSig
            EstadoSig = 0
            salida = False
            continue
        elif buscarCoincidencia(opcion,'0'): # Fecha de envio
            EstadoAnt = EstadoSig
            EstadoSig = 0
            salida = False
            continue
        else:
            print ("¿Puede reformular su pregunta?")
    if EstadoSig == 4: #Problemas con el pedido '1.1.2'
        categoria_id = '1.1.2.1'
        opcion = inputRespuesta()
        print("llegue aqui:)")
        if buscarCoincidencia(opcion,'1.1.2.2'): # Retardo
            EstadoAnt = EstadoSig
            EstadoSig = 0
            salida = False
            continue
        elif buscarCoincidencia(opcion,'1.1.2.3'): # Paquete dañado
            EstadoAnt = EstadoSig
            EstadoSig = 5
            salida = True
            continue
        elif buscarCoincidencia(opcion,'1.1.2.4'): # Paquete abierto
            EstadoAnt = EstadoSig
            EstadoSig = 5
            salida = True
            continue
        elif buscarCoincidencia(opcion,'1.1.2.5'): # No llego pedido
            EstadoSig = 5
            salida = True
            continue
        elif buscarCoincidencia(opcion,'1.1.2.6'): # Llego otro pedido
            EstadoSig = 5
            salida = True
            continue
        elif buscarCoincidencia(opcion,'1.1.2.7'): # Paquete Incompleto
            EstadoSig = 5
            salida = True
            continue
        elif buscarCoincidencia(opcion,'0'): # Direccion incorrecta
            EstadoAnt = EstadoSig
            EstadoSig = 5
            salida = True
            continue
        else:
            print ("¿Puede reformular su pregunta?")
    if EstadoSig == 6: #Soporte/Peidos/Cancelar
        categoria_id = '1.1.3.1'
        opcion = inputRespuesta()
        if buscarCoincidencia(opcion,'0'): # Razon
            EstadoAnt = EstadoSig
            EstadoSig = 0
            salida = False
        else:
             print ("¿Puede reformular su pregunta?")
    if EstadoSig == 7: #Soporte/Pedidos/ModificarDireccion
        categoria_id = '1.1.4.1'
        opcion = inputRespuesta()
        if buscarCoincidencia(opcion,'1.1.4.2'): # Modificar Direccion
            EstadoAnt = EstadoSig
            EstadoSig = 0
            salida = False
        elif buscarCoincidencia(opcion,'0'): # Fecha de envio
            EstadoAnt = EstadoSig
            EstadoSig = 5
            salida = False
        else:
             print ("¿Puede reformular su pregunta?")
    
    
        