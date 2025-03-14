import json
import requests
import time

# Configura tu API key de Deepseek
DEEPSEEK_API_KEY = 'sk-9f3783391ed648998d4fbd35cd246d49'

def get_deepseek_completion(categoria):
    """
    Obtiene la expresión regular y respuesta usando Deepseek API
    """
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        }

        prompt = f"""Eres un experto en chatbots. Dado el siguiente objeto JSON de una categoría de Amazon:
        {json.dumps(categoria, ensure_ascii=False)}
        
        Genera una expresión regular con palabras clave relacionadas (similar a "soporte|ayuda|soporte y ayuda|necesito|ayudame|ayudar|tecnico|duda") para que el chatbot pueda identificar la categoría y una respuesta humana y útil para el usuario.
        
        Responde solo con el JSON que incluya los campos "Expresion" y "Respuesta" completados."""

        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )

        # Imprimir la respuesta completa para debug
        print("Respuesta completa de la API:")
        print(response.text)
        
        if response.status_code == 200:
            response_json = response.json()
            print("\nContenido del mensaje:")
            print(response_json['choices'][0]['message']['content'])
            
            try:
                # Intentar extraer el JSON de la respuesta
                content = response_json['choices'][0]['message']['content']
                # Eliminar los marcadores de código markdown
                content = content.replace('```json', '').replace('```', '').strip()
                
                # Ahora intentar parsear el JSON limpio
                ai_response = json.loads(content)
                return ai_response.get("Expresion"), ai_response.get("Respuesta")
            except json.JSONDecodeError as e:
                print(f"Error al parsear JSON: {str(e)}")
                print(f"Contenido que se intentó parsear: {content}")
                return "", ""
        else:
            print(f"Error en la API de Deepseek: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return "", ""

    except Exception as e:
        print(f"Error al obtener respuesta de Deepseek: {str(e)}")
        return "", ""

def actualizar_expresiones():
    # Crear backup del archivo original
    try:
        with open('Expresiones_Juntas.json', 'r', encoding='utf-8') as f:
            expresiones = json.load(f)
            
        with open('Expresiones_Juntas_backup.json', 'w', encoding='utf-8') as f:
            json.dump(expresiones, f, ensure_ascii=False, indent=4)
            print("Backup creado exitosamente")
    except Exception as e:
        print(f"Error al crear backup: {str(e)}")
        return

    # Cargar archivos JSON
    with open('categorias.json', 'r', encoding='utf-8') as f:
        categorias = json.load(f)
    
    # Convertir expresiones a un diccionario para búsqueda más rápida
    expresiones_dict = {exp['nombre'].lower(): exp for exp in expresiones}
    
    # Lista para almacenar las expresiones actualizadas
    expresiones_actualizadas = []
    cambios = 0
    nuevas = 0
    
    # Procesar cada categoría
    for categoria in categorias:
        nombre = categoria['nombre'].lower()
        print(f"Procesando categoría: {nombre}")
        
        if nombre in expresiones_dict:
            # La categoría existe, verificar el ID
            expresion_existente = expresiones_dict[nombre]
            if expresion_existente['id'] != categoria['id']:
                # Actualizar el ID
                expresion_existente['id'] = categoria['id']
                cambios += 1
                print(f"ID actualizado para: {nombre}")
            expresiones_actualizadas.append(expresion_existente)
        else:
            # Nueva categoría, crear objeto y obtener expresión/respuesta de Deepseek
            nueva_expresion = {
                "nombre": categoria['nombre'],
                "id": categoria['id'],
                "Expresion": "",
                "Respuesta": ""
            }
            
            print(f"Generando expresión y respuesta para nueva categoría: {nombre}")
            expresion, respuesta = get_deepseek_completion(categoria)
            print(expresion, respuesta)
            nueva_expresion["Expresion"] = expresion
            nueva_expresion["Respuesta"] = respuesta
            
            expresiones_actualizadas.append(nueva_expresion)
            nuevas += 1
            
            # Esperar entre llamadas a la API
            time.sleep(2)
    
    # Guardar el resultado actualizado
    try:
        with open('Expresiones_Juntas.json', 'w', encoding='utf-8') as f:
            json.dump(expresiones_actualizadas, f, ensure_ascii=False, indent=4)
        
        print(f"\nProceso completado:")
        print(f"- Categorías actualizadas: {cambios}")
        print(f"- Categorías nuevas: {nuevas}")
        print(f"- Total de categorías: {len(expresiones_actualizadas)}")
        print(f"- Backup guardado en 'Expresiones_Juntas_backup.json'")
    except Exception as e:
        print(f"Error al guardar el archivo actualizado: {str(e)}")

if __name__ == "__main__":
    actualizar_expresiones()
