from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep  
import os
import dotenv

dotenv.load_dotenv()
path = os.getenv("LINK_FILE_1")


browse = webdriver.Chrome()

browse.get("https://www.chiletrabajos.cl/trabajos/informatica")

wait = WebDriverWait(browse, 10)  # Define wait with a timeout of 10 seconds

assert "Chiletrabajos" in browse.title

xpath = '//*[@id="buscador"]/div[5]/div['
xpath2 = ']/div[1]/h2/a'
mode = ""
if (os.path.exists(path)):
    mode = "a"
else:
    mode = "w"
    
    
print("Vigilar que no se cubra la pagina con popup, y cerrar de forma manual si aparece")
with open(path, mode) as file:
    if mode == "w":
        print("Creating file")
    else:
        print("Appending to file")
    # mientras limitado a solo 2 paginas,luego solo cambiar a j<=2 por  True
    j=1
    while True:
        print(f"Extracting page : {j}")
        for i in range(1, 31):
            try:
                sleep(2)
                elem = browse.find_element(By.XPATH, xpath + str(i) + xpath2)
                href = elem.get_attribute("href")
                file.write(href + "\n")
            except NoSuchElementException:
                print("Element not found, then no more pages, closing..")
                exit(0)
        j+=1
        # Intentar cerrar popup si aparece
        try:
            popup = WebDriverWait(browse, 5).until(
                EC.element_to_be_clickable((By.ID, "onesignal-slidedown-cancel-button"))
            )
            popup.click()
            print("Popup cerrado")
            sleep(2)
        except:
            print("No apareció popup")
        elem = elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a.page-link[data-ci-pagination-page='{j}']")))
        elem.click()
