from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


def scroll(driver, distance):
    js = f"var q=document.documentElement.scrollTop={distance}"
    driver.execute_script(js)
    time.sleep(0.5)

def single_choice(driver):
    questions = driver.find_elements(By.CSS_SELECTOR, '#div1 > div.ui-controlgroup.column1')
    for question in questions:
        options = question.find_elements(By.CSS_SELECTOR, '.ui-radio')
        random.choice(options).click()
        time.sleep(random.randint(0, 1))


def multiple_choice(driver):
    questions = driver.find_elements(By.CSS_SELECTOR, '#div2 > div.ui-controlgroup.column1')
    for question in questions:
        options = question.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
        num_choices = random.randint(1, len(options))
        selected_options = random.sample(options, num_choices)
        for option in selected_options:
            if not option.is_selected():
                option.click()
                time.sleep(random.randint(0, 1))


def fill_in_the_blank(driver, num):
    index = ["A", "B", "C"]
    answer = {"A": "python真的好用！", "B": "这个测试很成功！", "C": "填空题随机填写文本"}
    driver.find_element(By.CSS_SELECTOR, f'#q{num}').send_keys(answer.get(index[random.randint(0, len(index)-1)]))


def yanzheng(driver):
        try:
            # 出现点击验证码验证
            time.sleep(1)
            # 点击对话框的确认按钮
            driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
            # 点击智能检测按钮
            driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
            time.sleep(2)
        except:
            print("无验证")
        # 滑块验证
        try:
            slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
            if str(slider.text).startswith("请按住滑块"):
                width = slider.size.get('width')
                ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
        except:
            pass


def qd(times):
    url = 'https://www.wjx.cn/vm/ODYhzFn.aspx#'

    driver_path = r"D:\chromedriver_win32(1)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    for i in range(times):
        service = Service(driver_path)
        service.start()
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(url)
            single_choice(driver)
            multiple_choice(driver)
            scroll(driver, 600)
            fill_in_the_blank(driver, 3)
            time.sleep(random.randint(0, 1))#

            driver.find_element(By.CSS_SELECTOR, '#ctlNext').click()
            time.sleep(2)


            yanzheng(driver)

            print(f'已经提交了{i + 1}次问卷')
        except Exception as e:
            print(f'出现异常：{str}e')

        finally:
            driver.quit()
            service.stop()


if __name__ == "__main__":
    qd(60)

