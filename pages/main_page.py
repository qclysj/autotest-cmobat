from pages.base_page import BasePage
from pages.login_page import LoginPage


class MainPage(BasePage):

    url='https://www.jd.com/'

    login_button={'type':'link','value':'立即登录'}


    def open_url(self):
        self.open(self.url)
        self.wait()

    def go_to_login(self):
        self.click_element(self.login_button['type'],self.login_button['value'])
        return LoginPage()

