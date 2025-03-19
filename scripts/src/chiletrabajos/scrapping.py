from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from dataclasses import dataclass
from typing import List,Optional
import os
import dotenv

dotenv.load_dotenv()
path = os.getenv("LINK_FILE")

if (not os.path.exists(path) ):
    print(f"No file found in: {path}")
    exit(1)
links = []
with open(path, "r") as file:
    for line in file:
        links.append(line.strip())

class oferta:
    title:str
    salario: Optional[str]
    beneficios: Optional[str]
    empresa:str
    descripcion:str
    ubicacion:str
    fecha_publicacion:str
    fecha_expiracion:str
        
browse = webdriver.Chrome()
wait = WebDriverWait(browse, 10)  # Define wait with a timeout of 10 seconds
## links de prueba
## links = ["https://www.chiletrabajos.cl/trabajo/digitadores-3575698","https://www.chiletrabajos.cl/trabajo/desarrollador-backend-python-3582899"]
ofertas = [oferta() for _ in range(len(links))]
print(f"Extracting {len(links)} links")
for i in range (0,len(links)):
    browse.get(links[i])
    ofertas[i].title = browse.find_element(By.XPATH, '//*[@id="detalle-oferta"]/div[3]/h1').text
    ofertas[i].descripcion = browse.find_element(By.XPATH, '//*[@id="detalle-oferta"]/div[6]/div[2]/div[3]').text
    ofertas[i].empresa = browse.find_element(By.XPATH, '//*[@id="detalle-oferta"]/div[6]/div[1]/h3[1]/a[1]').text
    ofertas[i].ubicacion = browse.find_element(By.XPATH, "//td[contains(text(), 'Ubicación')]/following-sibling::td").text
    ofertas[i].fecha_publicacion = browse.find_element(By.XPATH, "//td[contains(text(), 'Fecha')]/following-sibling::td").text
    ofertas[i].fecha_expiracion = browse.find_element(By.XPATH, "//td[contains(text(), 'Expira')]/following-sibling::td").text
    try:
        ofertas[i].salario = browse.find_element(By.XPATH, "//td[contains(text(), 'Salario')]/following-sibling::td").text
    except:
        ofertas[i].salario = None
    try:
        content = browse.find_elements(By.CLASS_NAME, "beneficio-desc")
        contenido_beneficios = [b.text.strip() for b in content]
        beneficios = ""
        for content in contenido_beneficios:
            beneficios +=  "-" + content + "\n"
        ofertas[i].beneficios = beneficios
    except NoSuchElementException:
        ofertas[i].beneficios = None
    sleep(2)
print("Finished extracting data")
##
##
##  aca falta que hacer con los datos, por ejemplo guardarlos en un archivo o en una base de datos sql o no sql
##  falta preguntar
##
##