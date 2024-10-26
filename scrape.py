from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


def initialize_driver(chrome_path):
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service)
    return driver


def open_url(driver, url):
    driver.get(url)


def load_all_results(driver):
    while True:
        try:
            show_more_button = driver.find_element(By.XPATH, "//button[text()='Show more results']")
            
            if show_more_button.get_attribute("disabled"):
                print("All results loaded")
                break

            driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
            time.sleep(1)  # Allow time for scrolling animation
            
            show_more_button.click()
            print("Show more button clicked")
            time.sleep(2)
        
        except NoSuchElementException:
            print("No 'Show more results' button found or an error occurred.")
            break


def extract_perfume_data(driver, year):
    """Extract perfume data and return it as a list of dictionaries."""
    perfume_data = []
    perfumes = driver.find_elements(By.CLASS_NAME, 'card-section')

    for perfume in perfumes:
        try:
            link_element = perfume.find_element(By.TAG_NAME, 'a')
            perfume_link = link_element.get_attribute('href')
            perfume_name = link_element.text
            brand_element = perfume.find_element(By.TAG_NAME, 'small')
            brand_name = brand_element.text

            perfume_data.append({
                'Year': year,
                'Perfume Name': perfume_name,
                'Brand': brand_name,
                'Link': perfume_link
            })
        
        except NoSuchElementException:
            continue

    return perfume_data


def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def main(chrome_path, url, year):
    """Main function to initialize driver, load results, extract data, and save to CSV."""
    driver = initialize_driver(chrome_path)
    open_url(driver, url)
    
    load_all_results(driver)
    
    perfume_data = extract_perfume_data(driver, year)
    
    filename = f'perfumes_{year}.csv'
    save_to_csv(perfume_data, filename)
    
    driver.quit()


# Usage
chrome_path = r"C:\Users\Nick Olsz\Desktop\VSCode\chromedriver-win64\chromedriver.exe"

for year in range(2014, 2025):
    url = f"https://www.fragrantica.com/search/?godina={year}%3A{year}"
    main(chrome_path, url, year)
