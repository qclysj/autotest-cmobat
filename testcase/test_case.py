import logging
import pytest
import os
from datetime import datetime

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.search_page import SearchPage


# 获取当前日期和时间，用于生成文件名
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_name = f"test_log_{current_time}.logs"

# 创建日志目录（如果不存在）
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# 完整的日志文件路径
log_file_path = os.path.join(log_directory, log_file_name)

# 打印日志文件路径，验证是否正确
print(f"Log file path: {log_file_path}")

# 清理已有 handlers
root_logger = logging.getLogger()
for h in root_logger.handlers:
    root_logger.removeHandler(h)


# 配置日志记录到文件，同时输出到控制台

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]

)

# 测试日志配置是否生效
logging.info("This is a test log message")


class TestDemo:
    @pytest.mark.parametrize('username,password', [
        ('123', 'rightpwd'),
        ('rightusername', 'rightpwd'),
        ('rightusername', 'rightpwd')
    ])
    def test_01_login(self, username, password):
        try:
            print("Test login is running")  # 验证测试用例是否运行
            logging.info(f"Starting login test with username: {username}, password: {password}")
            main_page = MainPage()
            main_page.open_url()
            logging.info("Opened main page")
            main_page.go_to_login()
            logging.info("Navigated to login page")
            login_page = LoginPage()
            login_page.open_url()
            logging.info("Opened login page")
            login_page.login(username, password)
            logging.info("Login attempt completed")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise

    @pytest.mark.parametrize('text', [' ', 'iphone16promax'])
    def test_01_search(self, text):
        try:
            print("Test search is running")  # 验证测试用例是否运行
            logging.info(f"Starting search test with text: {text}")
            main_page = MainPage()
            main_page.open_url()
            logging.info("Opened main page")
            search_page = SearchPage()
            search_page.search(text)
            logging.info("Search attempt completed")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise


if __name__ == '__main__':
    pytest.main()
    logging.shutdown()
