# python3.6.5
# coding:utf-8

'''
@time:2019-02-16 16:50
使用步骤：
1、按格式输入商品链接和开售时间
2、程序自动打开chrome浏览器访问链接，跳至登陆页面请在30秒内扫码登陆
3、跳至商品页面请在开售时间前选择所有商品规格（如鞋码、配色）
4、开售后自动下单，在淘宝规定时间内完成支付
提示：
1、必须配合chrome浏览器（71-73版本）使用,只适用于淘宝和天猫
2、开售时间格式必须正确（xxxx-xx-xx(空格)xx:xx:xx）
4、扫码登陆后，chrome浏览器可能会拦截重定向请求，如发生请在浏览器地址栏末尾收到跳转网页
5、跳至商品页面，必须在开售时间前完成 全部 商品规格选择
6、提前设置默认邮寄地址和电话，中途无法更改
7、无法在下单页面操作，不适用使用优惠券等情况
8、程序打包后需要将chromedriver.exe放置在exe同目录下才能运行

程序利用自动测试工具模拟用户下单操作，完成商品的抢购
仅作为学习过程中的实践，无商业用途
'''

from selenium import webdriver
import datetime
import time

# 创建浏览器对象
driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
# 窗口最大化显示
driver.maximize_window()

def login(url, mall):
    '''
    登陆函数

    url:商品的链接
    mall：商城类别
    '''
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(2)
    # 淘宝和天猫的登陆链接文字不同
    if mall == '1':
        # 找到并点击淘宝的登陆按钮
        driver.find_element_by_link_text("亲，请登录").click()
    else:
        # 找到并点击天猫的登陆按钮
        driver.find_element_by_link_text("请登录").click()
    print("请在30秒内完成登录")
    # 用户扫码登陆
    time.sleep(30)

def buy(buy_time, mall):
    '''
    购买函数

    buy_time:购买时间
    mall:商城类别
    获取页面元素的方法有很多，获取得快速准确又是程序的关键
    在写代码的时候运行测试了很多次，css_selector的方式表现最佳
    '''
    if mall == '1':
        # "立即购买"的css_selector
        btn_buy = '#J_juValid > div.tb-btn-buy > a'
        # "立即下单"的css_selector
        btn_order = '#submitOrder_1 > div.wrapper > a'
    else:
        btn_buy = '#J_LinkBuy'
        btn_order = '#submitOrder_1 > div > a'

    while True:
        # 现在时间大于预设时间则开售抢购
        if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') > buy_time:
            try:
                # 找到“立即购买”，点击
                if driver.find_element_by_css_selector(btn_buy):
                    driver.find_element_by_css_selector(btn_buy).click()
                    break
                time.sleep(0.1)
            except:
                time.sleep(0.3)
    while True:
        try:
            # 找到“立即下单”，点击，
            if driver.find_element_by_css_selector(btn_order):
                driver.find_element_by_css_selector(btn_order).click()
                # 下单成功，跳转至支付页面
                print("购买成功")
                break
        except:
            time.sleep(0.5)

# https://detail.tmall.com/item.htm?spm=a21wu.10013406.0.0.509a35b6oV74DS&id=574581885483
if __name__ == "__main__":
    url = input("请输入商品链接:")
    mall = input("请选择商城（淘宝 1  天猫 2  输入数字即可）： ")
    bt = input("请输入开售时间【2019-02-15（空格）12:55:50】")
    login(url, mall)
    buy(bt, mall)

