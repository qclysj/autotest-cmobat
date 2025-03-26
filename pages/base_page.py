import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from drivers.driver_manager import driver

class BasePage():

    #打开网站
    def open(self,url):
        driver.get(url)


    #定位元素位置
    def find_element(self,type,value):
        if type=='id':
            el=driver.find_element(By.ID,value)
        elif type=='name':
            el=driver.find_element(By.NAME,value)
        elif type=='tag':
            el=driver.find_element(By.TAG_NAME,value)
        elif type=='class':
            el=driver.find_element(By.CLASS_NAME,value)
        elif type=='link':
            el=driver.find_element(By.LINK_TEXT,value)
        elif type=='plink':
            el=driver.find_element(By.PARTIAL_LINK_TEXT,value)
        elif type=='css':
            el=driver.find_element(By.CSS_SELECTOR,value)
        elif type=='xpath':
            el=driver.find_element(By.XPATH,value)
        else:
            print('输入的定位方式不正确')
        return  el

    #点击操作
    def click_element(self,type,value):
        self.find_element(type,value).click()

    #输入操作
    def input_element(self,type,value,text):
        self.find_element(type,value).send_keys(text)

    #鼠标悬停
    def move_mouse_to_element(self,type,value):
        ActionChains(driver).move_to_element(self.find_element(type,value)).pause(2).perform()

    #切换窗口
    def switch_to_window(self,title):
        handles=driver.window_handles
        for handle in handles:
            driver.switch_to.window(handle)
            if driver.title==title:
                break

    def wait(self):
        time.sleep(8)


