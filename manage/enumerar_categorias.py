import json

# Leer el archivo JSON
with open('categorias.json', 'r', encoding='utf-8') as file:
    categorias = json.load(file)

# Renumerar las categorías
for i, categoria in enumerate(categorias, 1):
    categoria['number'] = i

# Guardar el JSON actualizado
with open('categorias.json', 'w', encoding='utf-8') as file:
    json.dump(categorias, file, indent=4, ensure_ascii=False)

# Crear archivo txt con número y nombre
with open('categorias.txt', 'w', encoding='utf-8') as file:
    for categoria in categorias:
        file.write(f"{categoria['number']} {categoria['nombre']}\n")
