from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException


'''
我们可以用一种智能的方法来检测客户端重定向是否完成,首先从页面开始加载 时就“监视”DOM 中的一个元素,
然后重复调用这个元素直到 Selenium
抛出一个 StaleElementReferenceException 异常;
也就是说,元素不在页面的 DOM 里了,说明这时 网站已经跳转:
'''
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

driver = webdriver.PhantomJS(executable_path='<Path to Phantom JS>')
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
waitForLoad(driver)
print(driver.page_source)