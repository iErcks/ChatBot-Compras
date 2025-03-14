import json

# Leer ambos archivos
with open('categorias.json', 'r', encoding='utf-8') as file:
    categorias = json.load(file)

with open('Expresiones_Juntas.json', 'r', encoding='utf-8') as file:
    expresiones = json.load(file)

# Crear un diccionario para búsqueda rápida por ID
expresiones_dict = {exp['id']: exp for exp in expresiones}

# Actualizar las expresiones con los números de las categorías
for categoria in categorias:
    if categoria['id'] in expresiones_dict:
        expresiones_dict[categoria['id']]['number'] = categoria['number']

# Convertir el diccionario actualizado de vuelta a lista
expresiones_actualizadas = list(expresiones_dict.values())

# Guardar el resultado en un nuevo archivo
with open('Expresiones_Actualizadas.json', 'w', encoding='utf-8') as file:
    json.dump(expresiones_actualizadas, file, indent=4, ensure_ascii=False)
