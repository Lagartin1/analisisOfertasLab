from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep  
from dataclasses import dataclass
from typing import List,Optional
import os
import random
import dotenv
import re

dotenv.load_dotenv()
path = os.getenv("LINK_FILE_3")
path_out = os.getenv("CSV_INDEED")
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win32; x86) AppleWebKit/537.36")
browse = webdriver.Chrome(options=options)
wait = WebDriverWait(browse, 10) 
if path is None or not os.path.exists(path):
    print(f"No valid file path found or file does not exist: {path}")
    exit(1)
links = []
with open(path, "r") as file:
    for line in file:
        links.append(line.strip())
    
def detectar_captcha(browse):
    try:
        # Buscar el elemento main con clase 'error'
        main_error = browse.find_element(By.CSS_SELECTOR, "main.error")
        # Verificar contenido específico
        if "Additional Verification Required" in main_error.text:
            return True
            
        return False
        
    except NoSuchElementException:
        return False

with open(path_out, "a",encoding='utf-8') as file:
    i=0
    file.write("oferta;salario;empresa;descripcion;ubicacion\n")
    for link in links:
        browse.get(link)
        title, empresa, ubicacion, descripcion, salario = "", "", "", "", ""
        sleep(random.randint(2, 5))  # Sleep  random
        if detectar_captcha(browse):
            print("Captcha detectado,resolver manualmente \n")
            x = input("Presione Enter para continuar una vez resuelto el captcha...")
            sleep(random.randint(2, 5))  # Sleep  random  
        ## print(f"Extrayendo data en link n° {i} ")
        try:
            title+= browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div/h2').text
        except:
            try: 
                title += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[3]/div[1]/div[2]/h2').text
            except:
                try:
                    title += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/h2').text
                except :
                    print(f"No se encontró el título")
        descripcion += browse.find_element(By.XPATH, '//*[@id="jobDescriptionText"]').text
        descripcion = re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑ(){}|°\-&=%!¡¿+:*/$#]', '', descripcion)
        descripcion = descripcion.replace(';', '.')
        while ';' in descripcion:
            descripcion = descripcion.replace(';', '.')
        try:
            empresa += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div/div/span/a').text
        except:
            try:
                empresa += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/div/span').text
            except:
                try:
                    empresa += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div/div/span').text
                except:
                    empresa += "No se encontró la empresa"
                    print("No se encontró la empresa")
        ubicacion += browse.find_element(By.XPATH, '//*[@id="jobLocationText"]/div/span').text
        try:
            sueldo = browse.find_element(By.XPATH, '//*[@id="jobDetailsSection"]/div/div[1]/div[2]/div[1]/div/div/ul/li/div/div/div/div/span').text
            titulo_etiqueta = browse.find_element(By.XPATH, '//*[@id="jobDetailsSection"]/div/div[1]/div[2]/div[1]/div/h3').text.lower()
            if not ("sueldo" or "salario") in titulo_etiqueta:
                salario = "NaN"
            else:
                salario += sueldo
        except:
            salario = "NaN"
        i+=1
        file.write(f' "{title}";"{salario}";"{empresa}";"{descripcion}";"{ubicacion}"\n')
        
        # Barra de carga
        progress = (i / len(links)) * 100
        print(f"Progreso: {progress:.2f}% completado")
        # Limpiar barra de carga para la siguiente iteración
        print("\033[F\033[K", end="")  # Mover el cursor hacia arriba y limpiar la línea
        
print(f"Data extraida y guardada en: {path_out}")