from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains


driver = webdriver.PhantomJS(executable_path='/Users/xxg/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.implicitly_wait(5)
driver.get('http://github.com/xxg1413')
driver.get_screenshot_as_file('github.png')