import json
import re
import time
# Cargar el archivo JSON
with open('c:\\Users\\erick\\OneDrive\\Documentos\\ISC\\Semestre7\\MachineLearning\\ChatBot\\Expresiones_Juntas.json', 'r', encoding='utf-8') as file:
    mybd = json.load(file)


back = "si|regresar|retroceder|back"
si = "si|s|yes|y|claro|porfavor|adelante"
salir = "salir|exit|terminar|fin|cerrar|adios|chao|bye"


def cargar_categorias(ruta="Rangos.json"):
    with open(ruta, "r") as archivo:
        cat= json.load(archivo)  
    return {int(k): v for k, v in cat.items()}

categorias = cargar_categorias()

DiccEstados = {item["nombre"]: int(item["number"]) for item in mybd}



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



EstadoSig = 0
EstadoAnt = 0
Respuesta = ""
salida = True 

def inputRespuesta():
    opcion = input("Me: ").lower()
    return opcion

def buscarCoincidencia(opcion, categoria_id):
    global EstadoSig, EstadoAnt, Respuesta
    # Filtrar expresionesID para que solo contengan las coincidencias donde el id coincida exactamente con categoria_id
    expresionesID = {k: v for k, v in datos.items() if k == categoria_id}
    #print (f"Cateogria11: {categoria_id}")
    #print (f"Expresiones: {expresionesID}")
    for key, coincidencia in expresionesID.items():  # Corrección aquí
        #print (coincidencia)
        if re.search(coincidencia['Expresion'], opcion):
            #print(f"ChatBot: Tu interes es {coincidencia['nombre'].upper()} te dirigiremos al area correspondiente")
            EstadoAnt = EstadoSig
            EstadoSig = DiccEstados[coincidencia['nombre']]
            
            Respuesta = coincidencia['Respuesta']
            return True
    return False


def ImprimirCategorias(categorias):
    #print (categorias)
    for cat in categorias:
        if cat in datos:
            print(f"-: {datos[cat]['nombre']}")


def DirigeAEstado(categorias):
    global EstadoSig, EstadoAnt, salida, back, salir, Respuesta
    #print (f"Categorias: {categorias}")
    #print (f"EstadoActual: {EstadoSig}"
    print(f"ChatBot: {Respuesta}")
    ImprimirCategorias(categorias)
    if (len(categorias)) == 0:
        opcion = input("ChatBot: ¿Hay algo más en lo que te pueda ayudar? : ")
        if (re.search(si, opcion)):
            EstadoSig = 0
            EstadoAnt = 0
            Respuesta = "ChatBot: Soy tu ChatBot! en que puedo ayudarte?"
            return
        else:
            salida = False
            return
    opcion = inputRespuesta()

    
    if (re.search(back, opcion)): #regresar a estado anterior
        EstadoSig = EstadoAnt
        print("ChatBot: Regrese a la seccion anterior, ¿en puedo ayudarte?")
        Respuesta = ""
        
        return 
    if (re.search(salir, opcion)): #salir
        print("ChatBot: Gracias por usar nuestro chatbot")
        salida = False
        EstadoSig = -1
        return

    for n in categorias: #Buscar en la respuesta
        if buscarCoincidencia(opcion, n):
            return
        
    print("ChatBot: ¿No logre comprenderte, deseas volver al inicio?")
    if (re.search(back, input())): 
        EstadoSig = 0
        return 
    print("ChatBot: Replantea tu pregunta por favor")


def chatBot():
    global EstadoSig, EstadoAnt, salida, categorias
    while salida:
        DirigeAEstado(categorias[EstadoSig])
#print (DiccEstados['Rastreo'])
print("Bienvenido a nuestro chatbot")
Respuesta = "Soy tu ChatBot! en que puedo ayudarte?"
chatBot()
print("Gracias por usar Amazapan")
