from selenium import webdriver
import time


'''
那些使用了 Ajax 或 DHTML 技术改变 / 加载内容的页面,可能有一些采集手段,但是用 Python 解决这个问题只有两种途径:
直接从 JavaScript 代码里采集内容,或者用 Python 的 第三方库运行 JavaScript,直接采集你在浏览器里看到的页面

PhantomJS 无头浏览器

把 Selenium 和 PhantomJS 结合在一 起,就可以运行一个非常强大的网络爬虫了,
可以处理 cookie、JavaScrip、header,以及 任何你需要做的事情。
'''
driver = webdriver.PhantomJS(executable_path='')
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.close()