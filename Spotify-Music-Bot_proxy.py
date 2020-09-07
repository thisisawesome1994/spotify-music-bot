from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from random import randint
from time import sleep
import time
import os
import random
import argparse
parser = argparse.ArgumentParser()


#-db DATABSE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-c", "--cycles", help="Amount of cycles", type=int)
parser.add_argument("-t", "--min", help="Minimal Viewtime", type=int)
parser.add_argument("-m", "--max", help="Maximal Viewtime", type=int)
parser.add_argument("-u", "--username", help="user")
parser.add_argument("-p", "--password", help="pass")
parser.add_argument("-l", "--url", help="link")
parser.add_argument("-P", "--proxy", help="prox")
# parser.add_argument("-size", "--size", help="Size", type=int)

args = parser.parse_args()

for i in range(args.cycles):
    #proxy = random.choice(open('proxies.txt').readlines())
    useragent = random.choice(open('useragents.txt').readlines())
    opts1 = Options()
    opts1.add_argument('--user-agent=%s'% useragent)
    #opts1.add_argument('--mute-audio')
    opts1.add_argument('--incognito')
    opts1.add_argument('--proxy-server=%s'% args.proxy)
    #opts1.add_argument('--headless')
    opts1.add_argument('--start-maximized')
    browser1 = webdriver.Chrome(options=opts1)
    browser1.get(args.url)
    time.sleep(10)
    browser1.find_element_by_xpath(""" //*[@id="login-username"] """).send_keys(args.username)
    time.sleep(2)
    browser1.find_element_by_xpath(""" //*[@id="login-password"] """).send_keys(args.password)
    time.sleep(2)
    submit = browser1.find_element_by_xpath(""" //*[@id="login-button"] """)
    submit.click()
    time.sleep(15)
    play_button = browser1.find_element_by_xpath(""" //*[@id="main"]/div/div[2]/div[4]/div[1]/div/div[2]/div/div/div[2]/section/div[3]/div/button[1] """)
    time.sleep(2)
    play_button.click()
    time.sleep(randint(args.min, args.max))
    browser1.quit()
# script by thisisawesome1994