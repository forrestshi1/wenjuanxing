
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
"""
仅仅作为测试和自我学习使用，请不要用于学术作弊或者其他违法行为。
目前测试大约有10%的几率会出现异常，验证模块70%成功率，后续的会加入更多题型和概率优化。
如果想学习或者有操作的问题可以联系我
"""


#滚动页面到底层
def scroll(driver, distance):
    js = f"var q=document.documentElement.scrollTop={distance}"
    driver.execute_script(js)
    time.sleep(0.5)

#单选题
def single_choice(driver):
    questions = driver.find_elements(By.CSS_SELECTOR, '#div1 > div.ui-controlgroup.column1')
    for question in questions:
        options = question.find_elements(By.CSS_SELECTOR, '.ui-radio')
        random.choice(options).click()
        time.sleep(random.randint(0, 1))

#下拉框
def xialakuang(driver):
    # 找到下拉框元素
    driver.find_element(By.XPATH, '//*[@id="select2-q4-container"]').click()
    # 获取所有选项
    options = driver.find_elements(By.CSS_SELECTOR, '.select2-results__option')
    # 选择一个随机的选项
    random_index = random.randint(1, len(options) -1)
    random_option = options[random_index]
    # 点击选项
    random_option.click()




#多选题
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


#填空题，需要填写题号
def fill_in_the_blank(driver, num):
    index = ["A", "B", "C"]
    answer = {"A": "python真的好用！", "B": "这个测试很成功！", "C": "填空题随机填写文本"}
    driver.find_element(By.CSS_SELECTOR, f'#q{num}').send_keys(answer.get(index[random.randint(0, len(index)-1)]))


#解决验证
def yanzheng(driver):
        try:

            time.sleep(1)#等待验证弹出
            # 点击对话框的确认按钮
            driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
            time.sleep(4)#确认验证时间
            # 点击智能检测按钮
            driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
            time.sleep(4)#智能监测时间

        except:
            print("无验证")
        # 滑块验证 #目前来看滑块验证出现的概率很低，出现了一般可以直接关闭服务重新刷新来解决，还未遇到出现滑块的状况
        try:
            slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
            if str(slider.text).startswith("请按住滑块"):
                width = slider.size.get('width')
                ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
        except:
            pass

#启动！
def qd(times):
    url = 'https://www.wjx.cn/vm/ODYhzFn.aspx#'#传入问卷星的链接

    driver_path = r"D:\chromedriver_win32(1)\chromedriver.exe"#传入chromedriver的路径
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"#传入chrome的路径

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
            xialakuang(driver)
            time.sleep(random.randint(0, 1))#

            driver.find_element(By.CSS_SELECTOR, '#ctlNext').click()
            yanzheng(driver)
            time.sleep(2)



            print(f'已经提交了{i + 1}次问卷')
        except Exception as e:
            print(f'出现异常：{str}e')

        finally:
            driver.quit()
            service.stop()


if __name__ == "__main__":
    qd(60)

