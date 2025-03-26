

from pages.base_page import BasePage



class LoginPage(BasePage):
    url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
    input_username = {'type': 'id', 'value': 'loginname'}
    input_password = {'type': 'id', 'value': 'nloginpwd'}
    login_submit = {'type': 'id', 'value': 'loginsubmit'}

    def open_url(self):
        self.open(self.url)


    def login(self, username, password):
        self.input_element(self.input_username['type'], self.input_username['value'], username)
        self.input_element(self.input_password['type'], self.input_password['value'], password)
        self.click_element(self.login_submit['type'], self.login_submit['value'])



