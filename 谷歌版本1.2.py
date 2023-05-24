from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.common.by import By

"""
仅仅作为测试和自我学习使用，请不要用于学术作弊或者其他违法行为。
目前没有发现验证问题，涵盖市面90%主流题型，后续会更新ip地址的修改
如果想学习或者有操作的问题可以联系我
"""

# 滚动页面
def scroll(driver, distance):
    js = f"var q=document.documentElement.scrollTop={distance}"
    driver.execute_script(js)


# 单选题
def single_choice(driver,num):
    # 找到所有单选题
    questions = driver.find_elements(By.CSS_SELECTOR, f'#div{num} > div.ui-controlgroup.column1')
    for question in questions:
        options = question.find_elements(By.CSS_SELECTOR, '.ui-radio')
        weights = [3, 7]  # 第一个选项权重为7，第二个选项权重为3
        selected_option = random.choices(options, weights=weights)[0]
        selected_option.click()
        time.sleep(random.randint(0, 1))

# 下拉框
def xialakuang(driver,num):
    # 找到下拉框元素
    driver.find_element(By.XPATH, f'//*[@id="select2-q{num}-container"]').click()
    # 获取所有选项
    options = driver.find_elements(By.CSS_SELECTOR, '.select2-results__option')

    weights = [0,0.1,0.9] #默认第一个“请选择”不选,后面的为概率
    # 选择一个随机的选项
    random_option = random.choices(options, weights=weights)[0]
    # 点击选项
    random_option.click()
    time.sleep(random.randint(0, 1))

# 多选题
def multiple_choice(driver, num):
    # def multiple_choice(driver, num): 当要求设置组合概率时使用
    #     # 找到所有多选题
    #     questions = driver.find_elements(By.CSS_SELECTOR, f'#div{num} > div.ui-controlgroup.column1')
    #     for question in questions:
    #         options = question.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
    #
    #         # 为不同的选项组合设置不同的权重
    #         weighted_options = [
    #             (('A', 'B'), 10),
    #             (('B',), 90),
    #         ]
    #
    #         # 使用权重随机选择一个选项组合
    #         selected_option_combination = \
    #         random.choices(weighted_options, weights=[w for _, w in weighted_options], k=1)[0][0]
    #
    #         # 根据选择的选项组合选择选项
    #         for i, option in enumerate(options):
    #             option_text = option.text
    #             if option_text in selected_option_combination:
    #                 if not option.is_selected():
    #                     option.click()
    #                     time.sleep(random.randint(0, 1))

    #一般就用这个
        questions = driver.find_elements(By.CSS_SELECTOR, '#div2 > div.ui-controlgroup.column1')
        for question in questions:
            options = question.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
            num_choices = random.randint(1, len(options))
            selected_options = random.sample(options, num_choices)
            for option in selected_options:
                if not option.is_selected():
                    option.click()
                    time.sleep(random.randint(0, 1))



# 填空题
def fill_in_the_blank(driver, num):
    index = ["A", "B", "C"]
    answers = {"A": "python真的好用！", "B": "这个测试很成功！", "C": "填空题随机填写文本"}

    weights = [0, 0.5, 0.5]  # 按照顺序给每个答案分配权重值
    # 根据权重值选择答案
    selected_answer = random.choices(list(answers.values()), weights=weights)[0]
    # 填写相应的答案
    driver.find_element(By.CSS_SELECTOR, f'#q{num}').send_keys(selected_answer)

    time.sleep(random.randint(0, 1))

# 矩阵题
def juzhen(driver, num):
    num_dimensions = 2  # 设置维度的数量，根据实际情况进行调整

    weights_list = [
        [0, 0, 0,0.5,0.5],  # 第一个维度的选项权重列表
        [0.5, 0.5, 0,0,0]  # 第二个维度的选项权重列表
    ]

    for i in range(1, num_dimensions + 1):
        options = driver.find_elements(By.XPATH, f'//*[@id="drv{num}_{i}"]/td/a')
        weights = weights_list[i - 1]  # 根据当前维度的索引选择对应的权重列表

        selected_option = random.choices(options, weights=weights)[0]
        selected_option.click()

        time.sleep(random.randint(0, 1))



# 两表题
def liangbiao(driver, num):
    options = driver.find_elements(By.XPATH, f'//*[@id="div{num}"]/div[2]/div/ul/li')

    weights = [0, 0, 0,0.5,0.5]  # 分配选项的权重值，按照顺序与options列表对应

    selected_option = random.choices(options, weights=weights)[0]
    selected_option.click()
    time.sleep(random.randint(0, 1))

# 解决验证
def yanzheng(driver):
    try:
        time.sleep(1)  # 等待验证弹出
        # 点击对话框的确认按钮
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
        time.sleep(4)  # 确认验证时间
        # 点击智能检测按钮
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(4)  # 智能监测时间
    except:
        print("无验证")
    # 滑块验证
    # 目前来看滑块验证出现的概率很低，出现了一般可以直接关闭服务重新刷新来解决，还未遇到出现滑块的状况
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
    except:
        pass

# 启动！
def qd(times):
    url = 'https://www.wjx.cn/vm/e8pnohT.aspx# '  # 传入问卷星的链接
    # driver.set_window_size(600, 400) #设置窗口大小
    driver_path = r"D:\chromedriver_win32(1)\chromedriver.exe"  # 传入chromedriver的路径
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # 传入chrome的路径

    for i in range(times):
        # 躲避智能检测，将webDriver设置为false
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)

        service = Service(driver_path)
        service.start()
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(url)



            #运行区
            single_choice(driver, 1)
            multiple_choice(driver, 2)
            fill_in_the_blank(driver, 3)
            xialakuang(driver, 4)
            scroll(driver, 300)
            juzhen(driver, 5)
            scroll(driver, 600)
            liangbiao(driver,6)
            time.sleep(random.randint(0, 1))


            driver.find_element(By.CSS_SELECTOR, '#ctlNext').click()
            yanzheng(driver)
            time.sleep(2)

            print(f'已经提交了{i + 1}次问卷')
        except Exception as e:
            print(f'出现异常：{str(e)}')
        finally:
            driver.quit()
            service.stop()

if __name__ == "__main__":
    qd(2)
