#%%
from selenium import webdriver

def open_website(url):
    driver = webdriver.Chrome()
    driver.get(url)

