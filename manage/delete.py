import json
import re

def process_files():
    # Read the categories to remove from QUITAR.txt
    categories_to_remove = []
    with open('manage\quitar.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # Extract category name after the 3 digits and space
            match = re.match(r'\d{3}\s+(.*)', line.strip())
            if match:
                categories_to_remove.append(match.group(1).lower())

    # Read the JSON file
    with open('./Expresiones_Juntas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Keep track of removed categories
    removed_count = 0
    filtered_data = []

    # Filter out matching categories
    for item in data:
        if item['nombre'].lower() not in categories_to_remove:
            filtered_data.append(item)
        else:
            removed_count += 1

    # Write the filtered data back to the JSON file
    with open('Expresiones_Juntas.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"Proceso completado:")
    print(f"- Categorías eliminadas: {removed_count}")
    print(f"- Categorías restantes: {len(filtered_data)}")

if __name__ == "__main__":
    process_files()