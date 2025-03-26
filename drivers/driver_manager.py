import threading
from selenium import  webdriver
from selenium.webdriver.chrome.options import  Options as ChromeOptions
from selenium.webdriver.firefox.options import  Options as FirefoxOptions
from selenium.webdriver.edge.options import  Options as EdgeOptions


class DriverManager():
    def __init__(self,name='chrome'):
        if name=='chrome':
            option = ChromeOptions()
            option.add_experimental_option("detach", True)
            self.d = webdriver.Chrome(options=option)
        elif name=='firefox':
            option = FirefoxOptions()
            self.d = webdriver.Firefox(options=option)
        elif name=='edge':
            option=EdgeOptions()
            option.add_experimental_option("detach",True)
            self.d=webdriver.Edge(options=option)


driver=DriverManager().d


