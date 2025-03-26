import os
import time
import random
import logging
import platform
from configparser import ConfigParser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from selenium_stealth import stealth
def stealth_injection(driver):
    # 覆盖关键检测点
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = {runtime: {}};
        """
    })
# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('jd_auto.log'),
        logging.StreamHandler()
    ]
)


class JDAutoStealth:
    def __init__(self):
        self.driver = None
        self.config = self._load_config()
        self._init_driver()

    def _load_config(self):
        """加载配置文件"""
        config = ConfigParser()
        config.read('config.ini', encoding='utf-8')
        return {
            'account': config.get('Credentials', 'username'),
            'password': config.get('Credentials', 'password'),
            'headless': config.getboolean('Settings', 'headless', fallback=False),
            'proxy': config.get('Settings', 'proxy', fallback=None),
            'chrome_version': config.get('Settings', 'chrome_version', fallback=114)
        }

    def _init_driver(self):
        """初始化反检测浏览器"""
        try:
            options = uc.ChromeOptions()

            # 基础反检测配置
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-site-isolation-trials")
            options.add_argument(f"--window-size={random.randint(1200, 1920)},{random.randint(800, 1080)}")

            # 指纹混淆配置
            options.add_argument(f"--user-agent={self._generate_ua()}")
            options.add_argument("--use-angle=gl")  # 启用GPU加速

            # 代理配置
            if self.config['proxy']:
                options.add_argument(f"--proxy-server={self.config['proxy']}")

            # 无头模式
            if self.config['headless']:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")

            # 创建浏览器实例
            self.driver = uc.Chrome(
                options=options,
                version_main=int(self.config['chrome_version']),
                driver_executable_path='chromedriver' if platform.system() == 'Windows' else './chromedriver',
                patcher_force_close=True,
                suppress_welcome=True
            )

            # 注入反检测脚本
            stealth(driver=self.driver,
                    user_agent=options.arguments[4].split('=')[1],
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    run_on_insecure_origins=True)

            logging.info("浏览器初始化成功")
        except Exception as e:
            logging.error(f"浏览器初始化失败: {str(e)}")
            raise

    def _generate_ua(self):
        """生成随机User-Agent"""
        os_type = [
            '(Windows NT 10.0; Win64; x64)',
            '(Macintosh; Intel Mac OS X 10_15_7)',
            '(X11; Linux x86_64)'
        ]
        chrome_versions = [
            '114.0.5735.199', '115.0.5790.110',
            '116.0.5845.188', '117.0.5938.92'
        ]
        return f"Mozilla/5.0 {random.choice(os_type)} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"

    def _human_click(self, element):
        """人类化点击模拟"""
        try:
            actions = ActionChains(self.driver)

            # 随机移动路径
            for _ in range(random.randint(2, 5)):
                x = random.randint(-5, 5)
                y = random.randint(-5, 5)
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.1, 0.3))

            # 精确点击带偏移
            actions.move_to_element_with_offset(
                element,
                random.randint(-2, 2),
                random.randint(-2, 2)
            )
            actions.click()
            actions.perform()
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            logging.error(f"点击操作失败: {str(e)}")
            raise

    def _smart_wait(self, locator, timeout=15):
        """智能等待元素"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'})",
                element
            )
            time.sleep(random.uniform(0.3, 1.2))
            return element
        except TimeoutException:
            self.driver.execute_script("window.scrollBy(0, 200)")
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )

    def login(self):
        """登录流程"""
        try:
            self.driver.get("https://passport.jd.com/new/login.aspx")

            # 切换到账户登录
            self._human_click(self._smart_wait((By.LINK_TEXT, "账户登录")))

            # 输入账号
            username = self._smart_wait((By.ID, "loginname"))
            for char in self.config['account']:
                username.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            # 输入密码
            password = self._smart_wait((By.ID, "nloginpwd"))
            for char in self.config['password']:
                password.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))

            # 提交登录
            self._human_click(self._smart_wait((By.ID, "loginsubmit")))

            # 处理验证码
            if self._check_captcha():
                input("请手动完成验证码后按回车继续...")

            return True
        except Exception as e:
            logging.error(f"登录失败: {str(e)}")
            self._screenshot('login_error')
            return False

    def _check_captcha(self):
        """检查验证码"""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "captcha")))
        except:
            return False

    def search_product(self, keyword):
        """商品搜索"""
        try:
            search_box = self._smart_wait((By.ID, "key"))
            # 模拟人类输入
            for char in keyword:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.08, 0.25))
                if random.random() < 0.1:
                    search_box.send_keys(Keys.BACKSPACE)
                    time.sleep(0.2)
                    search_box.send_keys(char)

            # 随机等待后搜索
            time.sleep(random.uniform(0.5, 1.5))
            self._human_click(self._smart_wait((By.CSS_SELECTOR, "button.button")))
            return True
        except Exception as e:
            logging.error(f"搜索失败: {str(e)}")
            self._screenshot('search_error')
            return False

    def select_product(self, index=0):
        """选择商品"""
        try:
            products = self.driver.find_elements(By.CSS_SELECTOR, ".gl-item")
            if not products:
                raise Exception("未找到商品列表")

            # 随机选择商品
            target = products[random.randint(0, min(5, len(products) - 1))]
            self.driver.execute_script("arguments[0].scrollIntoView()", target)
            self._human_click(target)

            # 切换窗口
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return True
        except Exception as e:
            logging.error(f"商品选择失败: {str(e)}")
            self._screenshot('product_select_error')
            return False

    def add_to_cart(self):
        """加入购物车"""
        try:
            # 处理规格选择
            self._handle_specs()

            # 定位购物车按钮
            add_btns = [
                (By.ID, "InitCartUrl"),
                (By.CSS_SELECTOR, ".btn-addcart"),
                (By.XPATH, "//a[contains(text(),'加入购物车')]")
            ]

            for locator in add_btns:
                try:
                    btn = self._smart_wait(locator, timeout=8)
                    self._human_click(btn)
                    break
                except:
                    continue
            else:
                raise Exception("未找到购物车按钮")

            # 验证结果
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".msg-success"))
            )
            logging.info("成功加入购物车")
            return True
        except Exception as e:
            logging.error(f"加入购物车失败: {str(e)}")
            self._screenshot('cart_error')
            return False

    def _handle_specs(self):
        """处理商品规格"""
        try:
            specs = self.driver.find_elements(By.CSS_SELECTOR, ".item:not(.disabled)")
            if specs:
                random.choice(specs).click()
                time.sleep(random.uniform(0.5, 1.5))
        except:
            pass

    def _screenshot(self, name):
        """错误截图"""
        try:
            ts = int(time.time())
            self.driver.save_screenshot(f"error_{name}_{ts}.png")
        except:
            pass

    def run(self):
        """执行主流程"""
        try:
            if self.login():
                self.search_product("iPhone 16 Pro Max")
                if self.select_product():
                    if self.add_to_cart():
                        logging.info("流程执行成功")
                        time.sleep(5)
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    bot = JDAutoStealth()
    bot.run()