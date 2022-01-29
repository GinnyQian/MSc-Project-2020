# Theme2 + Firefox + Without filter

import os # Imports the os package
import requests # Imports the requests package
from selenium import webdriver # Imports the selenium package
import time # Imports the time package

class Theme2FirefoxWithout(object):
    def __init__(self):
        self.url = 'https://theme2zhenniqian.wordpress.com/'
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless') # set headless mode
        self.driver = webdriver.Firefox(options=options)
        self.driver.maximize_window()

        self.driver.implicitly_wait(20) # wait for 20s before throwing an exception

    def __del__(self):
        self.driver.close() # close the browser after finishing task

    def run(self, n=0):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"}
        response = requests.get(url=self.url, headers=headers)
        response.encoding = 'utf-8'
        self.driver.get(self.url)

        js = "window.scrollTo(0,150)"
        self.driver.execute_script(js) # scroll to the first green picture

        # traverse all the pictures for simulating user filtering green pictures
        time.sleep(3)

        pic_list = self.driver.find_elements_by_xpath(
            "//img[contains(@src,'https://theme2zhenniqian.files.wordpress.com/2021/07/green.jpg')]") # find all the green pictures

        if not os.path.exists('./pics-2FWT'):
            os.mkdir('./pics-2FWT') # set a folder for downloaded pictures

        for i in pic_list:
            n += 1 # set a counter for picture list
            img_src = i.find_element_by_xpath(
                "//img[contains(@src,'https://theme2zhenniqian.files.wordpress.com/2021/07/green.jpg')]").get_attribute(
                'src')
            img_name = 'pic' + str(n) + '.jpg'
            img_data = requests.get(url=img_src, headers=headers).content
            img_path = 'pics-2FWT/' + img_name

            with open(img_path, 'wb') as fp:
                fp.write(img_data)

            print(img_name, ' downloaded successfully!')

            if int(n) < len(pic_list) - 1:
                self.driver.execute_script("arguments[0].scrollIntoView();", pic_list[int(n) + 1]) # if downloading is not done, scroll to the next green picture
            else:
                js = "window.scrollTo(0,document.body.scrollHeight)"
                self.driver.execute_script(js) # if downloading is done, scroll to the bottom of the page

            time.sleep(2)

if __name__ == '__main__':
    theme2firefoxwithout = Theme2FirefoxWithout()
    theme2firefoxwithout.run()
