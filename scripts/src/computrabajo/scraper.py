import time
import json
import pandas as pd
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Selenium configuration and Chrome driver
chrome_options = Options()
# Change the User-Agent to simulate a real browser
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
#chrome_options.add_argument("--headless")  # To run the browser without a graphical interface
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the browser (Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

filename = "/home/rod/Documents/python-cc/links_computrabajo_p.txt"

# Función para leer un archivo y devolver los enlaces en una lista
def get_links(filename):
    try:
        with open(filename, 'r') as f:
            # Leer las líneas, eliminando espacios en blanco y saltos de línea innecesarios
            return set(line.strip() for line in f)
    except FileNotFoundError:
        print(f"El archivo {filename} no se encontró.")
        return set()

def extract_data(link):
    # Load the page
    driver.get(link)
    
    # Reduce the implicit wait time for the whole page
    driver.implicitly_wait(5)

    # Initialize default values
    salary_value = "NaN"
    company_name = "NaN"
    region = "NaN"
    commune = "NaN"
    job_title = "NaN"
    description = "NaN"

    try:
        # Esperar hasta que el bloque <script type="application/ld+json"> esté presente en la página
        script_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//script[@type='application/ld+json']"))
        )

        # Extraemos el contenido JSON del bloque <script>
        json_data = script_element.get_attribute('innerHTML')

        # Convertimos el contenido JSON en un diccionario de Python
        data = json.loads(json_data)

        salary_value = data['@graph'][2]['baseSalary']['value']['value']
        company_name = data['@graph'][2]['hiringOrganization']['name']
        region = data['@graph'][2]['jobLocation']['address']['addressLocality']
        commune = data['@graph'][2]['jobLocation']['address']['addressRegion']
        job_title = data['@graph'][2]['title']
        # Utilizamos XPath para acceder directamente al tercer objeto dentro de la clave "@graph" y obtener la descripción
        job_description = data['@graph'][2]['description']

        # Reemplazamos las etiquetas <br> por un espacio simple
        description = job_description.replace("<br/>", " ")
    except:
        pass
    
    if (salary_value == 0):
        salary_value = "NaN"

    r_string1 = "R."
    r_string2 = "Santiago - "
    
    if (r_string1 in region):
        region = region.replace(r_string1,"")
    if (r_string2 in commune):
        commune = commune.replace(r_string2,"")

    # Gather all extracted data
    job_data = {
        "Salario": salary_value,
        "Empresa": company_name,
        "Comuna": commune,
        "Región": region,
        "Cargo": job_title,
        "Descripción": description
    }
    
    return job_data

# Get links from .txt
all_links = get_links(filename)

# Create the DataFrame
data = []

c = 1

for link in all_links:
    job_data = extract_data(link)
    data.append(job_data)
    print(c,link)
    c += 1
    time.sleep(randint(527852,1527852)/1000000)

df = pd.DataFrame(data)

# Save the results to a CSV file
df.to_csv("/home/rod/Documents/python-cc/computrabajo_p25-30.csv", index=False)

# Close the browser
driver.quit()