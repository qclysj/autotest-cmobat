from login.Login import Login
from search.Search import Search
from purchase.Purchase import Purchase

import time
if __name__ == '__main__':
    login_obj=Login()
    driver=login_obj.login()
    Search(driver)
    Purchase(driver)

