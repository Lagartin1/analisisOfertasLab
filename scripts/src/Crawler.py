from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


browse = webdriver.Chrome()

browse.get("https://www.chiletrabajos.cl/trabajos/informatica")

wait = WebDriverWait(browse, 10)  # Define wait with a timeout of 10 seconds

assert "Chiletrabajos" in browse.title

xpath = '//*[@id="buscador"]/div[5]/div['
xpath2 = ']/div[1]/h2/a'
enlaces_card = []
j = 1
while j <= 2:
    for i in range(1, 48):
        sleep(1)
        elem = browse.find_element(By.XPATH, xpath + str(i) + xpath2)
        href = elem.get_attribute("href")
        enlaces_card.append(href)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a.page-link[data-ci-pagination-page='{j+1}']")))
    elem.click()
    j+=1
    
