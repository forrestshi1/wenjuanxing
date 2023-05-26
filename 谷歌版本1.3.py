import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.common.by import By
import requests
from fake_useragent import UserAgent



"""
仅仅作为测试和自我学习使用，请不要用于学术作弊或者其他违法行为。
目前没有发现验证问题，涵盖市面90%主流题型，后续会更新ip地址的修改
如果想学习或者有操作的问题可以联系我
"""


def get_random_proxy():
    # 定义代理服务器的API网址
    api_url = 'API地址'

    # 发送请求获取代理服务器
    response = requests.get(api_url)

    # 解析响应内容并随机选择一个IP地址和端口号
    ip_list1 = json.loads(response.text)['data']
    proxy_info = random.choice(ip_list1)
    random_ip = proxy_info['ip']
    random_port = proxy_info['port']

    # 格式化代理服务器
    proxy = {
        'http': f'http://{random_ip}:{random_port}',
        #'https': f'https://{random_ip}:{random_port}'
    }

    return proxy


# 滚动页面
def scroll(driver, distance):
    js = f"var q=document.documentElement.scrollTop={distance}"
    driver.execute_script(js)


# 单选题
def single_choice(driver,num,weights):
    # 找到所有单选题
    questions = driver.find_elements(By.CSS_SELECTOR, f'#div{num} > div.ui-controlgroup.column1')
    for question in questions:
        options = question.find_elements(By.CSS_SELECTOR, '.ui-radio')
        selected_option = random.choices(options, weights=weights)[0]
        selected_option.click()
        time.sleep(random.randint(0, 1))

# 下拉框
def xialakuang(driver,num,weights):
    # 找到下拉框元素
    driver.find_element(By.XPATH, f'//*[@id="select2-q{num}-container"]').click()
    # 获取所有选项
    options = driver.find_elements(By.CSS_SELECTOR, '.select2-results__option')


    # 选择一个随机的选项
    random_option = random.choices(options, weights=weights)[0]
    # 点击选项
    random_option.click()
    time.sleep(random.randint(0, 1))

# 多选题
def multiple_choice(driver, num):#概率待更新
    # 一般就用这个
        questions = driver.find_elements(By.CSS_SELECTOR, '#div2 > div.ui-controlgroup.column1')
        for question in questions:
            options = question.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
            num_choices = random.randint(1, len(options))
            selected_options = random.sample(options, num_choices)
            for option in selected_options:
                if not option.is_selected():
                    option.click()
                    time.sleep(random.randint(0, 1))
    # def multiple_choice(driver, num，weighted): 当要求设置组合概率时使用
    #     # 找到所有多选题
    #     questions = driver.find_elements(By.CSS_SELECTOR, f'#div{num} > div.ui-controlgroup.column1')
    #     for question in questions:
    #         options = question.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
    #
    #         # 为不同的选项组合设置不同的权重
    #         实例（在运行区这么写）weighted =[
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

# 填空题
def fill_in_the_blank(driver, num, answers, weights):

    # answers = ["python真的好用！", "这个测试很成功！", "填空题随机填写文本"]
    #
    # weights = [0, 0.5, 0.5]  # 按照顺序给每个答案分配权重值
    # 根据权重值选择答案
    selected_answer = random.choices(answers, weights=weights)[0]
    # 填写相应的答案
    driver.find_element(By.CSS_SELECTOR, f'#q{num}').send_keys(selected_answer)

    time.sleep(random.randint(0, 1))

# 矩阵题
def juzhen(driver, num, weights_list):
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
def liangbiao(driver, num, weights):
    options = driver.find_elements(By.XPATH, f'//*[@id="div{num}"]/div[2]/div/ul/li')
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
    url = 'https://www.wjx.cn/vm/e8pnohT.aspx'  # 传入问卷星的链接
    driver_path = r"D:\chromedriver_win32(1)\chromedriver.exe"  # 传入Chromedriver的路径
    options = webdriver.ChromeOptions()  # 别动这个
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # 传入chrome的路径
    options.add_argument("--disable-blink-features=AutomationControlled")#隐藏自动化，别动这个



    for i in range(times):
        headers = {
            "User-Agent": UserAgent().random
        }#随机UA
        #一定要先设置Ip!!!!!!!!!!!!!!!!
        proxy = get_random_proxy()
        print(f"正在使用代理IP {proxy['http']} ")

        # 设置请求头和代理服务器
        options.add_argument(f"user-agent={headers['User-Agent']}")
        options.add_argument(f"--proxy-server={proxy['http']}")

        service = Service(driver_path)
        service.start()
        driver = webdriver.Chrome(service=service, options=options)



        try:
            driver.get(url)
            #运行区，driver不要动，改后面的参数
            multiple_choice(driver, 2)
            single_choice(driver, 1,[1,0])

            fill_in_the_blank(driver, 3, ["python真的好用！", "这个测试很成功！", "填空题随机填写文本"], [0, 0.5, 0.5])
            xialakuang(driver, 4,[0,0.1,0.9])#概率第一个数默认为0，不要改
            scroll(driver, 300)
            juzhen(driver, 5,  [[0, 0, 0,0.5,0.5], [0.5, 0.5, 0,0,0]] )#不同维度的选项权重列表
            scroll(driver, 600)
            liangbiao(driver,6,[0, 0, 0,0.5,0.5])
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
    qd(5)
