"""This file is going to include method that will parse
the specific data that we need from each one of the boxes
"""
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.deal_boxes = boxes_section_element
        
    def deal_box_attributes(self):
        collections= []
        for deal_box in self.deal_boxes[:25]:
            hotel_name = deal_box.find_element_by_css_selector('div[data-testid="title"]').text
            hotel_price = deal_box.find_element_by_css_selector('span[data-testid="price-and-discounted-price"]').text
            try:
                hotel_score = deal_box.find_element_by_css_selector('div[data-testid="review-score"]').text.split('\n')[0]
            except NoSuchElementException:
                print('Review Score does not exist')
                hotel_score=''
            collections.append([hotel_name,hotel_price,hotel_score])
            # print('-'*20)
        return collections
            