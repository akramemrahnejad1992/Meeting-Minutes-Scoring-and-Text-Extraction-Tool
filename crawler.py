from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import re


def extract_date_from_url(url):
    # Extract the filename from the URL
    filename = url.split('FileName=')[-1]    
    # Define a regex pattern to match dates in the filename
    date_patterns = [
        r'(\d{1,2}\.\d{1,2}\.\d{2,4})', 
        r'(\w{3}\s\d{1,2}\s\d{2,4})'     
    ]
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            date_str = match.group(0)            
            # Convert to a datetime object
            try:
                # Handle different date formats
                if '.' in date_str:
                    date_obj = datetime.strptime(date_str, '%m.%d.%y')
                else:
                    date_obj = datetime.strptime(date_str, '%b %d %y')
                return date_obj
            except ValueError as e:
                print(f"ValueError: {e}")  
                continue
                
    return None 


def is_date_within_months(date_to_check, months):
    current_date = datetime.now()
    past_date_limit = current_date - relativedelta(months=months)
    return date_to_check <= past_date_limit
    
    
def crawl_links(url, class_name, tag=None, main_url=None):
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all(tag, class_=class_name) if tag else soup.find_all(class_=class_name)
    for item in items:
        if main_url:
            link = main_url + item.find('a')['href'].split('../..')[1]
            link_date = extract_date_from_url(link)
            if is_date_within_months(link_date, 18):
                print(link_date, 'Links are out of 18 months')
                break
        else:
            link = item.find('a')['href']
        links.append(link)
    return links

def get_links(driver, tag, class_name):
    links = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    for article in soup.find_all(tag, class_=class_name):
        link = article.find('a', href=True)
        if link:
            link_date = pd.to_datetime(link.text.split('-')[0])
            if is_date_within_months(link_date, 18):
                print(link_date, 'Links are out of 18 months')
                break
            links.append(link['href'])
    return links

def get_current_page(driver):
    current_page_element = driver.find_element(By.CSS_SELECTOR, 'a.ui-page-number-current-span[role="button"]')
    return int(current_page_element.text)

def get_page_links(driver, link, main_url):
    if 'ModuleInstanceID=2391' in link:
        tag = 'h1'
        page_links = get_links(driver, tag, 'ui-article-title')
        page_links = [main_url + link.split('../..')[1] for link in page_links]
    else:
        tag = 'h3'
        page_links = get_links(driver, tag, 'ui-article-title')
    return page_links

def click_next_page(driver, next_page):
    try:
        next_page_button = driver.find_element(By.CSS_SELECTOR, f'a[aria-label="Skip to Page {next_page}"]')
    except NoSuchElementException:
        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, f'a[aria-label="Go to Page {next_page}"]')
        except NoSuchElementException:
            raise Exception("No more pages...")

    driver.execute_script("arguments[0].click();", next_page_button)
    print(f'Clicked on: {next_page_button.text}')
    return True

def navigation(view_more_links, main_url):
    pages_links = []
    driver = webdriver.Chrome()
    
    for link in view_more_links:
        driver.get(link)  
        while True:
            time.sleep(2)  
            current_page = get_current_page(driver)
            print(f'Current Page: {current_page}')
            page_links = get_page_links(driver, link, main_url)
            pages_links.extend(page_links)

            next_page = current_page + 1
            
            try:
                click_next_page(driver, next_page)
            except Exception as e:
                print(e)
                break  

            time.sleep(4) 

    driver.quit()
    return pages_links
