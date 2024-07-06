"""This file is going to include method that will parse
the specific data that we need from each one of the boxes
"""
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pyautogui
import time
class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.deal_boxes = boxes_section_element
        

    def deal_box_attributes(self):
        collections= []
        for deal_box in self.deal_boxes[:75]:
            hotel_name = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
            hotel_price = deal_box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text
            
            score_elements = deal_box.find_elements(By.TAG_NAME, 'a')
            for element in score_elements:
                if element.get_attribute('data-testid')=="review-score-link":
                    hotel_score = element.text.split('\n')[0]
                    break
            else:
                hotel_score = ''
            collections.append([hotel_name, hotel_price, hotel_score])
            
        return collections
            