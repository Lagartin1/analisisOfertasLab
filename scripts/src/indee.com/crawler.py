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
import os
import random
import dotenv

dotenv.load_dotenv()
path = os.getenv("LINK_FILE_3")

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win32; x86) AppleWebKit/537.36")



browse = webdriver.Chrome(options=options)

browse.get("https://cl.indeed.com/jobs?q=inform%C3%A1tica&l=&from=searchOnHP%2Cwhatautocomplete&vjk=1a1acb3e470e94ee")

wait = WebDriverWait(browse, 10)  # Define wait with a timeout of 10 seconds

def human_like_wait():
    sleep(random.uniform(5, 10)) 
    
mode = ""
if (os.path.exists(path)):
    mode = "a"
else:
    mode = "w"
xpath_cards = '/html/body/main/div/div[2]/div/div[5]/div/div[1]/div[5]/div/ul/li['
xpath_cards2= ']/div/div/div/div/div/div/table/tbody/tr/td[1]/div[1]/h2/a'
sleep(10)
with open(path, mode) as file:
    if mode == "w":
        print("Creating file")
    else:
        print("Appending to file")
    j=1
    while True:
        print(f"Extracting page : {j}")
        try:
            sleep(2)
            # XPath relativo para encontrar todas las anclas objetivo
            target_xpath = ".//div/div/div/div/div/div/table/tbody/tr/td[1]/div[1]/h2/a"
            anchors = browse.find_elements(By.XPATH, "//ul/li//h2/a")
            human_like_wait()
            # Muestra href y texto
            i=0
            for a in anchors:
                i+=1
                file.write(a.get_attribute("href") + "\n")
            print(f"{i} elementos encontrados")
        except NoSuchElementException:
            print("No se encontraron elementos")
            break
        j += 1
        # pagina siguiente
        try:
            siguiente = browse.find_element(By.XPATH, "//a[@aria-label='Página siguiente']")
            siguiente.click()
            print("Pagina siguiente")
            sleep(5)
        except NoSuchElementException:
            print("No hay mas paginas")
            exit(0)