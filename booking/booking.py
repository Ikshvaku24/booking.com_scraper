from selenium import webdriver
import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

from prettytable import PrettyTable
import os 

class Booking(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/Drivers', teardown = False):
        self.driver_path = driver_path
        os.environ['PATH']+=self.driver_path
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Booking,self).__init__(options=options)
        # print(Booking.mro()) #method resolution order read about it with super
        self.implicitly_wait(15)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            return super().__exit__()    
    
    def land_first_page(self):
        self.get(const.BASE_URL)
        
    def exit_signup(self):
        try:
            wait = WebDriverWait(self, 10)  # Wait for up to 10 seconds
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')))
            button.click()
        except TimeoutException:
            print("The button was not clickable within the timeout period")
            
    def change_currency(self,currency):
        currency_element = self.find_element(By.CSS_SELECTOR,'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()
        
        selected_currency_element = self.find_element(By.XPATH,f'//div[text()="{currency}"]')
        selected_currency_element.click()
        
        wait = WebDriverWait(self,5)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'button[data-testid="header-currency-picker-trigger"]'),currency))
    
    def select_place_to_go(self, place_to_go):
        # Retry locating the first autocomplete result in case of a stale element
        for _ in range(3):  # Retry up to 3 times
            try:
                wait = WebDriverWait(self, 3)
                # Find the search field
                search_field = wait.until(EC.presence_of_element_located((By.NAME, 'ss')))
                # search_field = self.find_element_by_name('ss')
                search_field.clear()
                # Send keys to the search field
                search_field.send_keys(place_to_go)
                wait.until(lambda self: search_field.get_attribute('value') == place_to_go)
                # wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@id="group-0-heading" and text()="Popular destinations nearby"]')))
                wait.until(lambda self: not self.find_element(By.CSS_SELECTOR, 'ul[role="group"]').get_attribute('aria-labelledby'))
                first_element = self.find_element(By.CSS_SELECTOR,
                    'li[id="autocomplete-result-0"]'
                )
                first_element.click()
                break  # Exit loop if click is successful
            except StaleElementReferenceException:
                print("StaleElementReferenceException caught. Retrying...")
                # Re-locate the search field and retry if necessary
    
    def select_date(self,check_in_date,check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR,
            f'span[data-date="{check_in_date}"]'
        )
        check_in_element.click()
        
        check_out_element = self.find_element(By.CSS_SELECTOR,
            f'span[data-date="{check_out_date}"]'
        )
        check_out_element.click()
        
    def select_adults(self, count = 1):
        selection_element= self.find_element(By.CSS_SELECTOR,'span[data-testid="searchbox-form-button-icon"]')
        selection_element.click()
        
        
        
        adult_element = self.find_element(By.XPATH,'//input[@id="group_adults"]/parent::div')
        while(True):
            decrease_adults_element =  adult_element.find_element(By.XPATH,'.//button[1]')
            decrease_adults_element.click()
            adult_element_value = int(self.find_element(By.ID,'group_adults').get_attribute('value'))
            if adult_element_value == 1:
                break
        
        increase_adults_element = adult_element.find_element(By.XPATH,'.//button[2]')

        for _ in range(count-1):
            increase_adults_element.click()
        
    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR,'button[type="submit"]')
        search_button.click()
        
    def apply_filtration(self):
        filtration = BookingFiltration(self)
        filtration.apply_star_rating(1,2,3)
        filtration.sort_price_lowest_first()
    
    def report_results(self):
        import time
        table = PrettyTable(
            field_names= ["Hotel Name","Hotel Price","Hotel Score"]
        )
        desired_number_of_rows = 125  # Define how many rows you want to collect
        current_row_count = 0
       
        while current_row_count < desired_number_of_rows:
        
            hotel_boxes = WebDriverWait(self,10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'div[data-testid="property-card-container"]'))
                )
            self.execute_script(f"window.scrollTo(0,document.body.scrollHeight-800);")
            
            
            
            report = BookingReport(hotel_boxes[current_row_count:])
                # print(report.deal_box_attributes())
            new_data = report.deal_box_attributes()
            table.add_rows(new_data[:desired_number_of_rows])
            current_row_count = len(table.rows)
            
            print(f"Current number of rows: {current_row_count}")
            if current_row_count>=desired_number_of_rows:
                break
            # Break if there are no more new elements being loaded
            if len(new_data)==0:
                try:
                    load_more_button = self.find_element(By.XPATH,'//span[text()="Load more results"]')
                    if load_more_button.is_displayed():
                        load_more_button.click()
                        WebDriverWait(self, 10).until(EC.staleness_of(load_more_button))
                except NoSuchElementException:
                    break  # No more load more button and no new elements
                except TimeoutException:
                    break
                        
            
        print(table)
        print(len(table._rows))
        with open('hotels.csv','w') as f:
            f.write(table.get_csv_string())
        while True:
            pass
        
        
        