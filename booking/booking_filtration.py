"""
This file will include instance methods.
That will be reponsible to interact with our website.
After we have some results to apply filtrations.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        
    def apply_star_rating(self, *star_vals):
        # Waiting for page to completely load 
        WebDriverWait(self.driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,'button[data-testid="header-currency-picker-trigger"]'))
    )
        star_filtration_box = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id^="filter_group_class_"]'))
    )   
        for _ in range(3):
            try:
                star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR,'*')
                break
            except StaleElementReferenceException:
                star_filtration_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[id^="filter_group_class_"]'))
            ) 
        else:
            raise Exception("Failed to locate star_child_elements after retries")
        
        for star_val in star_vals:
            for star_element in star_child_elements:
                s_letter = 's' if star_val>1 else ''
                #staleness
                for _ in range(3):
                    try:
                        star_element_innerHTML = star_element.get_attribute('innerHTML')
                        break
                    except StaleElementReferenceException:
                        star_element_innerHTML = star_element.get_attribute('innerHTML')
                        
                if str(star_element_innerHTML).strip() == f'{star_val} star{s_letter}':
                    star_element.click()
                    WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,f'input[name="{star_val} star{s_letter}"]')))
                   
                    
                    
    
    def sort_price_lowest_first(self):
        
        sort_by_dropdown = self.driver.find_element(By.CSS_SELECTOR,'button[data-testid="sorters-dropdown-trigger"]').click()
        price_lowest_to_highest = self.driver.find_element(By.CSS_SELECTOR,'button[data-id="price"]').click()
    
    
        