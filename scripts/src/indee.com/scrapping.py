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

dotenv.load_dotenv()
path = os.getenv("LINK_FILE_3")
path_out = os.getenv("CSV_INDEED")
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win32; x86) AppleWebKit/537.36")
browse = webdriver.Chrome(options=options)
wait = WebDriverWait(browse, 10)  # Define wait with a timeout of 10 seconds
if path is None or not os.path.exists(path):
    print(f"No valid file path found or file does not exist: {path}")
    exit(1)
links = []
with open(path, "r") as file:
    for line in file:
        links.append(line.strip())

    
i=0
with open(path_out, "a",encoding='utf-8') as file:
    file.write("oferta;salario;empresa;descripcion;ubicacion\n")
    for link in links:
        browse.get(link)
        title, empresa, ubicacion, descripcion, salario = "", "", "", "", ""
        if (i == 0 or i == 388):
            x = input("Precione Enter si ya paso el captcha...\n ")
        print(f"Extrayendo data en link n° {i} ")
        sleep(random.randint(2, 5))  # Sleep for a random time between 1 and 3 seconds 
        try:
            title+= browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div/h2').text
        except:
            try: 
                title += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[3]/div[1]/div[2]/h2').text
            except:
                try:
                    title += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/h2').text
                except Exception as e:
                    print(f"No se encontró el título:{e}")
                    exit (1)
        descripcion += browse.find_element(By.XPATH, '//*[@id="jobDescriptionText"]').text
        try:
            empresa += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div/h3/a').text
        except:
            try:
                empresa += browse.find_element(By.XPATH, '//*[@id="jobLocationText"]/div/span').text
            except:
                try:
                    empresa += browse.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[3]/div[1]/div[2]/div/span/a').text
                except:
                    empresa += "No se encontró la empresa"
                    print("No se encontró la empresa")
        ubicacion += browse.find_element(By.XPATH, '//*[@id="jobLocationText"]/div/span').text
        try:
            salario += browse.find_element(By.XPATH, '//*[@id="jobDetailsSection"]/div/div[1]/div[2]/div[1]/div/div/ul/li/div/div/div/div/span').text
        except:
            salario += 'Nan'
        i+=1
        file.write(f"{title};{salario};{empresa};{descripcion};{ubicacion}\n")
        
        sleep(random.randint(1, 5))  # Sleep for a random time between 1 and 3 seconds        
        
        
        
print(f"Data extraida y guardada en: {path_out}")