import json

import numpy  # 新加的
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.common.by import By
import requests
from fake_useragent import UserAgent
import multiprocessing

"""
仅仅作为测试和自我学习使用，请不要用于学术作弊或者其他违法行为。
作者；forrest
"""


def get_random_proxy():
    # 定义代理服务器的API网址
    api_url = 'https://service.ipzan.com/core-extract?num=1&no=20230525165982903521&minute=1&format=json&area=220000&repeat=1&protocol=1&pool=ordinary&mode=whitelist&secret=uvg8pco497ldfag'

    # 发送请求获取代理服务器
    response = requests.get(api_url)

    # 解析响应内容并随机选择一个IP地址和端口号
    ip_list1 = json.loads(response.text)['data']['list']
    proxy_info = random.choice(ip_list1)
    random_ip = proxy_info['ip']
    random_port = proxy_info['port']

    # 格式化代理服务器
    proxy = {
        'http': f'http://{random_ip}:{random_port}',
        # 'https': f'https://{random_ip}:{random_port}'
    }

    return proxy


# 滚动页面
def scroll(driver, distance):
    js = f"var q=document.documentElement.scrollTop={distance}"
    driver.execute_script(js)


# 单选题
def single_choice(driver, num, weights):
    # 找到所有单选题

    questions = driver.find_elements(By.CSS_SELECTOR, f'#div{num} > div.ui-controlgroup.column1')
    for question in questions:
        options = question.find_elements(By.CSS_SELECTOR, '.ui-radio')
        if weights == -1:
            weights = [1] * len(options)
        selected_option = random.choices(options, weights=weights)[0]
        selected_option.click()
        time.sleep(random.randint(0, 1))

def two_choice(driver, num, weights):
    # 找到所有单选题
    # div1 > div.ui-controlgroup.two_column
    questions = driver.find_elements(By.CSS_SELECTOR, f'#div{num} > div.ui-controlgroup.two_column')
    for question in questions:
        options = question.find_elements(By.CSS_SELECTOR, '.ui-radio')
        if weights == -1:
            weights = [1] * len(options)
        selected_option = random.choices(options, weights=weights)[0]
        selected_option.click()
        time.sleep(random.randint(0, 1))



# 下拉框
def xialakuang(driver, num, weights):
    # 找到下拉框元素
    driver.find_element(By.XPATH, f'//*[@id="select2-q{num}-container"]').click()
    # 获取所有选项
    options = driver.find_elements(By.CSS_SELECTOR, '.select2-results__option')
    if weights == -1:
        weights = [0] + [1] * (len(options) - 1)

    # 选择一个随机的选项
    random_option = random.choices(options, weights=weights)[0]
    # 点击选项
    random_option.click()
    time.sleep(random.randint(0, 1))




# 多选题
def multiple_choice(driver, num, weights, n=None):
    xpath = f'//*[@id="div{num}"]/div[2]/div'
    options = driver.find_elements(By.XPATH, xpath)
    # 第current题对应的概率值
    mul_list = []
    if len(options) != len(weights):
        print(f"第{num}题概率值和选项值不一致")
    # 保证必有至少一个被选中
    while sum(mul_list) <= 0:
        mul_list = []
        for (index, item) in enumerate(weights):
            a = numpy.random.choice(a=numpy.arange(0, 2), p=[1 - (item / 100), item / 100])
            mul_list.append(a)
    if n:
        while sum(mul_list) > n:
            a = random.choice([i for i, x in enumerate(mul_list) if x == 1])
            mul_list[a] = 0
    for (index, item) in enumerate(mul_list):
        if item == 1:
            driver.find_element(By.CSS_SELECTOR,
                                f"#div{num} > div.ui-controlgroup > div:nth-child({index + 1})").click()

def multiple_choice1(driver, num):
    # 一般就用这个
        questions = driver.find_elements(By.CSS_SELECTOR, f'#div{num} > div.ui-controlgroup.column1')
        for question in questions:
            options = question.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
            num_choices = random.randint(1, len(options))
            selected_options = random.sample(options, num_choices)
            for option in selected_options:
                if not option.is_selected():
                    option.click()
                    time.sleep(random.randint(0, 1))


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
def juzhen(driver, num, weights_list, num_dimensions):
    #num_dimensions # 设置维度的数量，根据实际情况进行调整

    for i in range(1, num_dimensions + 1):
        options = driver.find_elements(By.XPATH, f'//*[@id="drv{num}_{i}"]/td/a')
        weights = weights_list[i - 1]  # 根据当前维度的索引选择对应的权重列表
        if weights == -1:
            weights = [1] * len(options)

        selected_option = random.choices(options, weights=weights)[0]
        selected_option.click()

        time.sleep(random.randint(0, 1))


# 两表题
def liangbiao(driver, num, weights):
    options = driver.find_elements(By.XPATH, f'//*[@id="div{num}"]/div[2]/div/ul/li')
    if weights == -1:
        weights = [1] * len(options)
    selected_option = random.choices(options, weights=weights)[0]
    selected_option.click()
    time.sleep(random.randint(0, 1))


# 解决验证
def yanzheng(driver):
    try:
        time.sleep(2)  # 等待验证弹出
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
        if str(slider.text).startswith("请按住滑块，拖动到最右边"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
    except:
        pass
    try:
        time.sleep(2)  # 等待验证弹出
        # 点击智能检测按钮
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(4)  # 智能监测时间
    except:
        pass
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块，拖动到最右边"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
    except:
        pass


# 启动！
def qd(times):
    url = 'https://www.wjx.cn/vm/e8pnohT.aspx'  # 传入问卷星的链接
    driver_path = r"E:\py tools\driver\edgedriver_win64\msedgedriver.exe"  # 传入edgedriver的路径
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 传入edge的路径

    for i in range(times):
        headers = {
            "User-Agent": UserAgent().random
        }  # 随机UA，别动这个

        # 设置Ip!!!!!!!!!!!!!!!!，如果需要代理，把下面的代码取消注释，全选后按 ctrl+/ 即可
        # proxy = get_random_proxy()
        # print(f"正在使用代理IP {proxy['http']} ")
        # options.add_argument(f"user-agent={headers['User-Agent']}")
        # options.add_argument(f"--proxy-server={proxy['http']}")

        # 启动浏览器，别动下面的代码
        service = Service(driver_path)
        service.start()
        driver = webdriver.Edge(service=service, options=options)

        try:
            driver.get(url)
            # 运行区，driver不要动，改后面的参数
            # 改括号里面的内容，其中driver不要动，第一个数字代表题号 裂开吗，
            # 关于概率，每个选项都要设置权重，可以看单选题的注释示例，[1,3]和[10,30]是没有区别的.

            # -1表示随机概率
            single_choice(driver, 1, [1, 3])  # [1,3]代表第一个选项被选择的概率为1/1+3，第二个选项被选择的概率为3/1+3
            multiple_choice1(driver, 2)  # 多选题，选项随机选择
            fill_in_the_blank(driver, 3, ["python真的好用！", "这个测试很成功！", "填空题随机填写文本"],
                              [0, 0.5, 0.5])  # 填空题,第二个参数为填写的文本列表，第三个参数代表每个文本被填写的概率
            xialakuang(driver, 4, -1)  # 概率第一个数默认为0，不要改.从[0.1,0.9]开始修改，在我的例子中代表选项6和选项7被选择的概率为0.1和0.9
            scroll(driver, 300)  # 滚动条，加不加其实都行
            juzhen(driver, 5, [[0, 0, 0, 0.5, 0.5], [0.5, 0.5, 0, 0, 0]],2)  # 不同维度的选项权重列表
            scroll(driver, 600)  # 滚动条，加不加其实都行
            liangbiao(driver, 6, [0, 0, 0, 0.5, 0.5])  # 量表题，选项权重列表

            time.sleep(10000)  # 随机等待时间，不要动

            time.sleep(random.randint(0, 1))  # 随机等待时间，不要动

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
    if __name__ == '__main__':
        # 创建多个进程
        processes = []
        for i in range(1):  # range里面的数字代表进程数，即开几个浏览器窗口
            p = multiprocessing.Process(target=qd, args=(1,))  # 第一个参数为提交次数
            processes.append(p)
            p.start()

        # 等待所有进程结束
        for p in processes:
            p.join()