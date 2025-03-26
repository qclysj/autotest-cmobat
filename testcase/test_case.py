import os
import time

import  pytest


from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.search_page import SearchPage
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TestDemo():
    @pytest.mark.parametrize('username,password',
                             [('123', 'pang20040207'),
                             ('18292830257', '12345'),
                             ('18292830257', 'pang20040207')])
    def test_01_login(self,username,password):
        main_page=MainPage()
        main_page.open_url()
        main_page.go_to_login()
        login_page=LoginPage()
        login_page.open_url()
        login_page.login(username,password)
        try:
            login_page.login(username,password)
            assert login_page.is_login_successful(),'Login failed'
        except Exception as e:
            print(f'An error occuredduring login:{e}')
    @pytest.mark.parametrize('text',[' ','iphone16promax'])
    def test_01_search(self,text):
        main_page=MainPage()
        main_page.open_url()
        search_page=SearchPage()
        search_page.search(text)
        try:
            search_page.search(text)
            assert search_page.is_search_successful(),'Login failed'
        except Exception as e:
            print(f'An error occuredduring search:{e}')








if __name__ == '__main__':
    pytest.main()

