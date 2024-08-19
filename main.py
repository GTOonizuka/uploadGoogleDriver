import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pywinauto
from pywinauto.keyboard import send_keys
from pywinauto import Application
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
#禁止自動關閉瀏覽器
options.add_experimental_option("detach",True)
#將自動化標頭去掉
options.add_experimental_option('excludeSwitches',["enable-automation"])
options.add_experimental_option('useAutomationExtension',False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-extensions')
options.add_argument('--no--sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')
#禁止"保存密碼"彈出框
options.add_experimental_option("prefs",{"credentials_enable_service":False,"profile.password_manager_enabled":False})

#gmail帳號
account_email = ""
#gmail密碼
password = ''
#圖片檔案位置輸入範例:"C:\\圖片\\test.jpg"
file_path = ''

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com.tw/")
driver.maximize_window()

#登入的操作
def login():
    
    try:
        #前往首頁
        driver.get("https://www.google.com.tw/")
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.XPATH,"//span[contains(text(),'登入')]")
            )
        )
        #點擊登入按鈕
        login_btn = driver.find_element(By.CSS_SELECTOR,'.gb_va').click()
        time.sleep(1)
        
        #定位到'輸入電子信箱框'
        login_email = driver.find_element(By.XPATH,"//input[@type='email']").send_keys(account_email)
        time.sleep(1)
        
        #定位到帳號的下一步按鈕
        login_account_next_step = driver.find_element(By.ID,"identifierNext").click()
        time.sleep(3)
        
        #定位到輸入密碼
        login_password = driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
        time.sleep(1)
        
        #定位到點擊密碼的下一步
        login_password_next_step = driver.find_element(By.ID,"passwordNext").click()
        time.sleep(1)
        
    except TimeoutError:
        print("等待逾時")
        time.sleep(3)
        driver.quit()
login()
time.sleep(1)

#點擊選單按鈕
menu = driver.find_element(By.XPATH, "//a[@aria-label='Google 應用程式']")
menu.click()

#定位到選單的iframe
menu_iframe = driver.find_element(By.XPATH ,"//*[@id='gb']/div/div[3]/iframe")

#切換到選單的iframe
driver.switch_to.frame(menu_iframe)
time.sleep(3)

#定位到menu裡面的雲端硬碟按鈕
menu_google_driver = driver.find_element(By.XPATH,"//*[@id='yDmH0d']/c-wiz/div/div/c-wiz/div/div/div[2]/div[2]/div[1]/ul/li[11]/a/span")

#點擊雲端硬碟按鈕
menu_google_driver.click()
time.sleep(5)

#切回到默認的HTML
driver.switch_to.default_content()

#定位到新增按鈕
addition = driver.find_element(By.XPATH, "//span[contains(text(),'新增')]")
time.sleep(5)

#點擊新增按鈕
addition.click()
time.sleep(5)

#使用WebDriverWait來等待元素可見,再去查找"檔案上傳"元素
#EC.presence_of_element_located 是 Selenium WebDriver 中的一個等待條件，用於確保在頁面上存在指定的元素。
upload_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@data-tooltip='檔案上傳']"))
)

# 使用 JavaScript 確保元素可見
driver.execute_script("arguments[0].scrollIntoView();", upload_button)

# 點擊檔案上傳
upload_button.click()

time.sleep(3)

#檔案上傳窗口連接
app = Application(backend='win32').connect(title='開啟')
pop_window = app['開啟']


#確認檔案上傳這個窗口存在
try:
    pop_window['檔案名稱(N)：Edit'].type_keys(file_path)
    time.sleep(3)
    pop_window['開啟(O)'].click()
except Exception as e:
    print(f"操作失败: {e}")

time.sleep(3)

sys.exit()
