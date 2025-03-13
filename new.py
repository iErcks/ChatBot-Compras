import json
import re

# Cargar el archivo JSON
with open('c:\\Users\\erick\\OneDrive\\Documentos\\ISC\\Semestre7\\MachineLearning\\ChatBot\\Expresiones_Juntas.json', 'r', encoding='utf-8') as file:
    mybd = json.load(file)


back = "si|volver|regresar|retroceder|back"
si = "si|s|yes|y|claro|porfavor|adelante"
salir = "salir|exit|terminar|fin|cerrar|adios|chao|bye"


def cargar_categorias(ruta="categorias.json"):
    with open(ruta, "r") as archivo:
        cat= json.load(archivo)  
    return {int(k): v for k, v in cat.items()}

categorias = cargar_categorias()

# Filtrar y obtener los datos del JSON de soporte
datos = {}  # Diccionario con toda la base de datos del JSON

# Guardar todo el JSON en un diccionario
for expresion in mybd:
    #print (expresion)
    datos[expresion['id']] = {
        'nombre': expresion['nombre'],
        'Expresion': expresion['Expresion'],
        'Respuesta': expresion['Respuesta']
    }


DiccEstados = {}

DiccEstados = {
    'soporte y ayuda': 1,
    'pedidos': 2,
    'Seguimiento': 3,
    'Problemas': 4,
    'Rastreo': 5,
    'Cancelar pedido': 6,
    'Modificar direccion': 7
}

EstadoSig = 0
EstadoAnt = 0
Respuesta = ""
salida = True 

def inputRespuesta():
    opcion = input("Explica tu asunto: ")
    return opcion

def buscarCoincidencia(opcion, categoria_id):
    global EstadoSig, EstadoAnt, Respuesta
    expresionesID = {k: v for k, v in datos.items() if k.startswith(categoria_id)}
    for key, coincidencia in expresionesID.items():  # Corrección aquí
        if re.search(coincidencia['Expresion'], opcion):
            print(f"Tu asunto es -{coincidencia['nombre']}- te dirigiremos al area correspondiente")
            EstadoAnt = EstadoSig
            EstadoSig = DiccEstados[coincidencia['nombre']]
            Respuesta = coincidencia['Respuesta']
            return True
    return False

def volver():
    global EstadoSig, EstadoAnt
   
    return 

def DirigeAEstado(categorias):
    global EstadoSig, EstadoAnt, salida, back, salir
    opcion = inputRespuesta()

    
    if (re.search(back, opcion)): #regresar a estado anterior
        EstadoSig = EstadoAnt
        print("Regrese a la seccion anterior, ¿en puedo ayudarte?")
        return 
    if (re.search(salir, opcion)): #salir
        print("Gracias por usar nuestro chatbot")
        salida = False
        EstadoSig = -1
        return

    for n in categorias: #Buscar en la respuesta
        if buscarCoincidencia(opcion, n):
            return
        
    print("¿No logre comprenderte, deseas volver?")
    if (re.search(back, input())): 
        EstadoSig = EstadoAnt
        return 
    print("Replantea tu pregunta por favor")

def UltimoEstado():
    global Respuesta
    global salida
    global EstadoSig 
    print(Respuesta)
    #print("¿Hay algo más en lo que te pueda ayudar?")
    if (re.search(si, input())):
        print("Claro, ¿En qué puedo ayudarte?")
        EstadoSig = 0
        return
    salida = False





def chatBot():
    global EstadoSig
    global EstadoAnt
    global salida
    global categorias
    while salida:
        if EstadoSig == 0: #Estado inicial 
            DirigeAEstado(categorias[0])
        if EstadoSig == 1: #soporte
            DirigeAEstado(categorias[1])
        if EstadoSig == 2: #soporte/pedidos
            DirigeAEstado(categorias[2])
        if EstadoSig == 3: #soporte/pedidos/seguimiento
            DirigeAEstado(categorias[3])
        if EstadoSig == 4: #soporte/pedidos/seguimiento respuestas
            DirigeAEstado(categorias[4])
        if EstadoSig == 5: 
            UltimoEstado()
        if EstadoSig == 6: #soporte/Pedidos/Canclear
            DirigeAEstado(categorias[6])
        if EstadoSig == 7: #Soporte/Pediddos/ModificarReembolso
            DirigeAEstado(categorias[7])
        

print("Bienvenido a nuestro chatbot")
chatBot()
print("Gracias por usar nuestro chatbot")