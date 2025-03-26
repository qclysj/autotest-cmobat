# import threading
# from selenium import  webdriver
# from selenium.webdriver.chrome.options import  Options as ChromeOptions
# from selenium.webdriver.firefox.options import  Options as FirefoxOptions
# from selenium.webdriver.edge.options import  Options as EdgeOptions
#
#
# class DriverManager():
#     def __init__(self,name='chrome'):
#         if name=='chrome':
#             option = ChromeOptions()
#             option.add_experimental_option("detach", True)
#             self.d = webdriver.Chrome(options=option)
#         elif name=='firefox':
#             option = FirefoxOptions()
#             self.d = webdriver.Firefox(options=option)
#         elif name=='edge':
#             option=EdgeOptions()
#             option.add_experimental_option("detach",True)
#             self.d=webdriver.Edge(options=option)
#
#
# driver=DriverManager().d



#driver单例化实现
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class DriverManager():
    _instance=None
    _lock=threading.Lock()
    _initialized=False


    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, name='edge'):
        if not self._initialized:
             if name=='chrome':
                 option = ChromeOptions()
                 option.add_experimental_option("detach", True)
                 self.driver = webdriver.Chrome(options=option)
             elif name=='firefox':
                 option = FirefoxOptions()
                 self.driver = webdriver.Firefox(options=option)
             elif name=='edge':
                 option=EdgeOptions()
                 option.add_experimental_option("detach",True)
                 self.driver=webdriver.Edge(options=option)
        self._initialized=True
driver=DriverManager().driver
