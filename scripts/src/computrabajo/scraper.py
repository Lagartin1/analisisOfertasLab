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

NUMBER_OF_PAGES = 10 # Number of pages to go through to extract links

# Selenium configuration and Chrome driver
chrome_options = Options()
# Change the User-Agent to simulate a real browser
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
#chrome_options.add_argument("--headless")  # To run the browser without a graphical interface
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the browser (Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Access the website
driver.get("https://cl.computrabajo.com/trabajo-de-desarrollador")

# Wait for the page to load
time.sleep(5)

def extract_links():
    # Find the JSON content within the <script type="application/ld+json"> tag
    script_element = driver.find_element(By.CSS_SELECTOR, "script[type='application/ld+json']")
    
    # Extract the content of the script
    json_data = script_element.get_attribute("innerHTML")
    
    # Parse the JSON
    data = json.loads(json_data)
        
    # Extract the links from the 'itemListElement' array
    links = []
    
    # Check if the JSON contains the '@graph' key
    if '@graph' in data:
        # Iterate through the elements inside '@graph'
        for item in data['@graph']:
            # If the 'itemListElement' key exists, iterate through it
            if 'itemListElement' in item:
                for element in item['itemListElement']:
                    # If there is a 'url' field, add it to the list of links
                    if 'url' in element:
                        links.append(element['url'])
    
    return links
    
    # Show the extracted links
    #print("Links found:")
    #for link in links:
    #    print(link)

# Function to navigate to the next page
def go_to_next_page():
    try:
        # Find the "Next" button and get the link to the next page
        next_button = driver.find_element(By.XPATH, '//span[@title="Siguiente"]')
        next_page_url = next_button.get_attribute('data-path')  # Get the value of the data-path attribute
        
        if next_page_url:
            driver.get(next_page_url)  # Load the next page using the link
            time.sleep(3)  # Wait a bit for the new page to load
        else:
            print("No more pages.")
            return False
    except Exception as e:
        print(f"Error while navigating to the next page: {e}")
        return False
    return True

all_links = []

for i in range(NUMBER_OF_PAGES):
    all_links = all_links + extract_links()
    go_to_next_page()

#print(all_links)

def extract_data(link):
    # Load the page
    driver.get(link)
    
    # Reduce the implicit wait time for the whole page
    driver.implicitly_wait(5)

    # Initialize default values
    salary_value = "N/A"
    company_name = "N/A"
    region = "N/A"
    commune = "N/A"
    job_title = "N/A"

    try:
        # Extract Salary
        salary_element = driver.find_element(By.XPATH, '//span[@itemprop="baseSalary"]/meta[@itemprop="value"]')
        salary_value = salary_element.get_attribute("content")
    except:
        pass

    try:
        # Extract Company
        company_element = driver.find_element(By.XPATH, '//span[@itemprop="hiringOrganization"]/meta[@itemprop="name"]')
        company_name = company_element.get_attribute("content")
    except:
        pass

    try:
        # Extract Region and Commune
        location_element = driver.find_element(By.XPATH, '//span[@itemprop="jobLocation"]/span[@itemprop="address"]')
        region = location_element.find_element(By.XPATH, './/meta[@itemprop="addressLocality"]').get_attribute("content")
        commune = location_element.find_element(By.XPATH, './/meta[@itemprop="addressRegion"]').get_attribute("content")
    except:
        pass

    try:
        # Extract Job Title
        title_element = driver.find_element(By.XPATH, '/html/body/main/span/meta[1]')
        job_title = title_element.get_attribute('content')
    except:
        pass
    
    # Gather all extracted data
    job_data = {
        "Salario": salary_value,
        "Empresa": company_name,
        "Comuna": commune,
        "Región": region,
        "Cargo": job_title
    }
    
    return job_data

# Create the DataFrame
data = []

for link in all_links:
    job_data = extract_data(link)
    data.append(job_data)
    print(link)
    time.sleep(randint(527852,1527852)/1000000)

df = pd.DataFrame(data)

# Save the results to a CSV file
df.to_csv("../../data/computrabajo/computrabajo2.csv", index=False)

# Close the browser
driver.quit()