# import threading
# from selenium import  webdriver
# from selenium.webdriver.chrome.options import  Options as ChromeOptions
# from selenium.webdriver.firefox.options import  Options as FirefoxOptions
# from selenium.webdriver.edge.options import  Options as EdgeOptions
#
#
# class DriverManager():
#     _instance=None
#     _lock=threading.Lock()
#     def __init__(self,name='chrome'):
#         if DriverManager._instance is not None:
#             raise Exception("This class is a singleton！Use instance() instead")
#             with DriverManager._lock:
#                 if DriverManager._instance is None:
#                     self.name=name
#                     if name=='chrome':
#                         option = ChromeOptions()
#                         option.add_experimental_option("detach", True)
#                         self.d = webdriver.Chrome(options=option)
#                     elif name=='firefox':
#                         option = FirefoxOptions()
#                         self.d = webdriver.Firefox(options=option)
#                     elif name=='edge':
#                         option=EdgeOptions()
#                         option.add_experimental_option("detach",True)
#                         self.d=webdriver.Edge(options=option)
#
#
# driver=DriverManager().d
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class DriverManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, name='chrome'):
        if DriverManager._instance is not None:
            raise Exception("This class is a singleton! Use instance() instead.")
        with DriverManager._lock:
            if DriverManager._instance is None:
                self.name = name
                if name == 'chrome':
                    option = ChromeOptions()
                    option.add_experimental_option("detach", True)
                    self.driver = webdriver.Chrome(options=option)
                elif name == 'firefox':
                    option = FirefoxOptions()
                    self.driver = webdriver.Firefox(options=option)
                elif name == 'edge':
                    option = EdgeOptions()
                    option.add_experimental_option("detach", True)
                    self.driver = webdriver.Edge(options=option)
                else:
                    raise ValueError("Unsupported browser name")
                DriverManager._instance = self

    @classmethod
    def instance(cls, name='chrome'):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(name)
        return cls._instance

    def __del__(self):
        self.driver.quit()

# 使用示例
driver = DriverManager.instance('chrome')
# 进行测试操作...
# 当不再需要时，可以手动调用 __del__ 方法来关闭浏览器
# del driver
