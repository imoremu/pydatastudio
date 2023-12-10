'''
Created on 18 nov. 2018

@author: imoreno
'''
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pydatastudio import resourcesmanager
import os

drivers = {}

CHROME = "chrome"
FIREFOX = "firefox"

CHROME_DRIVER_FILE = resourcesmanager.get_resource_path(os.path.join(".", "bin", "chromedriver.exe"))

def get_driver_from_name (name, browser_type = CHROME):
    
    if not name in drivers.keys():
        
        if (browser_type == FIREFOX):
        
            caps = DesiredCapabilities.FIREFOX.copy()
            caps['marionette'] = False
            drivers[name] = webdriver.Firefox(capabilities=caps)
            
        else:
            
            drivers[name] = webdriver.Chrome(CHROME_DRIVER_FILE)
        
    return drivers[name]