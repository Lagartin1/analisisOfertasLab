import time
import json
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

#NUMBER_OF_PAGES = 2  # Número de páginas para recorrer y extraer enlaces
SEARCH_URLS = [
    "https://cl.computrabajo.com/trabajo-de-software"
]  # Lista de URLs de búsqueda

# Configuración de Selenium y Chrome driver
chrome_options = Options()
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inicializar el navegador (Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def extract_links():
    # Buscar el contenido JSON dentro de la etiqueta <script type="application/ld+json">
    script_element = driver.find_element(By.CSS_SELECTOR, "script[type='application/ld+json']")
    
    # Extraer el contenido del script
    json_data = script_element.get_attribute("innerHTML")
    
    # Parsear el JSON
    data = json.loads(json_data)
    
    # Extraer los enlaces de la lista 'itemListElement'
    links = []
    
    if '@graph' in data:
        for item in data['@graph']:
            if 'itemListElement' in item:
                for element in item['itemListElement']:
                    if 'url' in element:
                        links.append(element['url'])
    
    return links

def go_to_next_page():
    try:
        # Buscar el botón "Siguiente" y obtener el enlace a la siguiente página
        next_button = driver.find_element(By.XPATH, '//span[@title="Siguiente"]')
        next_page_url = next_button.get_attribute('data-path')
        
        if next_page_url:
            driver.get(next_page_url)  # Cargar la siguiente página usando el enlace
            time.sleep(uniform(2.94, 6.12))  # Esperar un poco para que cargue la nueva página
        else:
            print("No hay más páginas.")
            return False
    except Exception as e:
        print(f"Error al navegar a la siguiente página: {e}")
        return False
    return True

# Recopilar enlaces de todas las páginas para las 3 búsquedas
all_links = set()  # Usamos un conjunto para evitar enlaces duplicados

for search_url in SEARCH_URLS:
    driver.get(search_url)
    time.sleep(uniform(4.8, 5.2))  # Esperar que la página cargue

    links_on_page = extract_links()  # Extraer los enlaces de la página
    all_links.update(links_on_page)  # Añadir los enlaces a la lista sin duplicados

    while go_to_next_page():
        links_on_page = extract_links()  # Extraer los enlaces de la página
        all_links.update(links_on_page)  # Añadir los enlaces a la lista sin duplicados

# Mostrar el número de enlaces encontrados
print(f"Enlaces encontrados: {len(all_links)}")

# Guardar los enlaces en un archivo .txt
with open("links_computrabajo_test2_parte3.txt", "w") as file:
    for link in all_links:
        file.write(link + "\n")

# Cerrar el navegador
driver.quit()
