import pdfplumber
import json
import re

def extract_categories_from_pdf():
    categories = []
    number_counter = 1
    
    # Abrir el PDF
    with pdfplumber.open('manage\categorias.pdf') as pdf:
        # Procesar cada página
        for page in pdf.pages:
            text = page.extract_text()
            # Dividir el texto en líneas
            lines = text.split('\n')
            
            # Procesar cada línea
            for line in lines:
                # Buscar patrones de numeración (1., 1.1, 1.1.1, etc.)
                match = re.match(r'(\d+(?:\.\d+)*)\.\s+(.+)', line.strip())
                if match:
                    # Extraer el ID completo y el nombre
                    category_id = match.group(1)  # Esto capturará "1.6.14.2"
                    category_name = match.group(2).strip()
                    
                    
                    # Crear el objeto de categoría
                    category = {
                        "id": category_id,
                        "nombre": category_name,
                        "number": number_counter
                    }
                    
                    categories.append(category)
                    number_counter += 1
    
    # Guardar en archivo JSON
    with open('categorias.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)
    
    print(f"Se han extraído {len(categories)} categorías y se han guardado en categorias.json")
    return categories

if __name__ == "__main__":
    try:
        categories = extract_categories_from_pdf()
        # Mostrar las primeras 5 categorías como ejemplo
        print("\nPrimeras 5 categorías extraídas:")
        for category in categories[:5]:
            print(f"ID: {category['id']}, Number: {category['number']}, Nombre: {category['nombre']}")
    except Exception as e:
        print(f"Error al procesar el PDF: {str(e)}")