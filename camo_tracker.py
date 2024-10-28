import requests
from lxml import html
import json
import pandas as pd

# URL
URL = "https://game8.co/games/Call-of-Duty-Black-Ops-6/archives/470430"

# Ruta del archivo JSON
JSON_FILE_PATH = "categories.json"

# XPaths
TABLE_XPATH = "/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/div[2]/table/tbody/tr"
WEAPON_XPATH_1 = ".//td[3]/a/text()"
WEAPON_XPATH_2 = ".//td[3]/text()"
CHALLENGE_XPATH = ".//td[4]/text()"
TYPE_XPATH = ".//td[5]/text()"


# Función para obtener el contenido de la página
def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Error al acceder a la página:", response.status_code)
        return None


# Función para extraer y limpiar el texto
def extract_text(row, primary_xpath, fallback_xpath=None):
    elements = row.xpath(primary_xpath)
    if elements:
        return elements[0].strip()
    elif fallback_xpath:
        # Intentar con el XPath alternativo si el primero falla
        elements = row.xpath(fallback_xpath)
        return elements[0].strip() if elements else ""
    return ""


# Función para analizar los datos de la tabla usando XPath
def parse_table_data(content):
    # Parsear
    tree = html.fromstring(content)

    # Seleccionar la tabla
    rows = tree.xpath(TABLE_XPATH)

    data = []

    for row in rows:
        # Extraer la información de cada columna especificada
        weapon = extract_text(row, WEAPON_XPATH_1, WEAPON_XPATH_2)
        challenge = extract_text(row, CHALLENGE_XPATH)
        type_ = extract_text(row, TYPE_XPATH)

        # Almacenar los datos extraídos en un diccionario
        item = {
            "Weapon": weapon,
            "Challenge": challenge,
            "Camo": type_,
        }

        data.append(item)
    return data


# Añadir la categoria
def add_category_column(existing_data):
    # Cargar el JSON
    with open(JSON_FILE_PATH, "r") as file:
        data = json.load(file)

    # Crear un diccionario
    weapon_to_category = {
        weapon: item["category"] for item in data for weapon in item["weapons"]
    }

    # Iterar sobre cada arma
    for item in existing_data:
        weapon = item.get("Weapon")
        # Buscar la categoría en el diccionario y asignar "Unknown" si no se encuentra
        item["Category"] = weapon_to_category.get(weapon, "Unknown")

    return existing_data


# Guardar en un archivo Excel
def save_to_excel(data, filename="camo_tracker.xlsx"):
    df = pd.DataFrame(data)

    # Reordenar las columnas
    columns_order = ["Category", "Weapon", "Camo", "Challenge"]
    df = df.reindex(columns=columns_order)

    # Ordenar según "Category" y luego "Weapon"
    df = df.sort_values(by=["Category", "Weapon"])

    # Guardar
    df.to_excel(filename, index=False)
    print(f"Datos guardados en {filename}")


#
def main():
    content = fetch_page_content(URL)
    if content:
        camo_data = parse_table_data(content)
        updated_data = add_category_column(camo_data)
        save_to_excel(updated_data)


#
if __name__ == "__main__":
    main()
