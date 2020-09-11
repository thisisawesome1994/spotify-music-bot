from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as selEc
from selenium.webdriver.common.by import By as selBy
from selenium.webdriver.support.ui import WebDriverWait
import json, time, threading, random, sys
from modules.spotify import links, xpaths
#parser = argparse.ArgumentParser()


#-db DATABSE -u USERNAME -p PASSWORD -size 20
#parser.add_argument("-c", "--cycles", help="Amount of cycles", type=int)
#parser.add_argument("-t", "--min", help="Minimal Viewtime", type=int)
#parser.add_argument("-m", "--max", help="Maximal Viewtime", type=int)
#parser.add_argument("-u", "--username", help="user")
#parser.add_argument("-p", "--password", help="pass")
#parser.add_argument("-l", "--url", help="link")
#parser.add_argument("-P", "--proxy", help="prox")
# parser.add_argument("-size", "--size", help="Size", type=int)

#args = parser.parse_args()

def run(username, password, _url, _headless):

    # Open Chrome and head to playlist link
    
    #proxy = random.choice(open('proxies.txt').readlines())
    useragent = random.choice(open('useragents.txt').readlines())
    opts1 = Options()
    opts1.headless = _headless
    opts1.add_argument('--user-agent=%s'% useragent)
    #opts1.add_argument('--mute-audio')
    opts1.add_argument('--incognito')
    #opts1.add_argument('--headless')
    opts1.add_argument('--start-maximized')
    browser = webdriver.Chrome(executable_path='drivers/chromedriver.exe', options=opts1)
    wait = WebDriverWait(browser, 35)
    browser.get(_url) if _url else browser.get(links["default"])
    
    # Login with given credentials
    
    user_form = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["user_form"])))
    user_form.send_keys(username)
    pass_form = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["pass_form"])))
    pass_form.send_keys(password)
    cookie_check = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["cookie_check"])))
    cookie_check.click()
    submit_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["submit_btn"])))
    submit_btn.click()
    
    # Configure shuffle and repeat settings
    shuffle_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["shuffle_btn"])))
    repeat_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["repeat_btn"])))
    
    # Activate shuffle if disabled
    if "control-button--active" not in shuffle_btn.get_attribute("class"):
        time.sleep(1)
        shuffle_btn.click()
    
    # Set repeat mode to "playlist"
    if "spoticon-repeat-16 control-button--active" in repeat_btn.get_attribute("class"):
        pass
    elif "spoticon-repeatonce-16 control-button--active" in repeat_btn.get_attribute("class"):
        time.sleep(1)
        repeat_btn.click()
        time.sleep(1)
        repeat_btn.click()
    else:
        time.sleep(1)
        repeat_btn.click()
    
        # Start playing
    play_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["play_btn"])))
    play_btn.click()
    while True:
        time.sleep(random.randint(89, 121))
        song_name = wait.until(selEc.presence_of_element_located((selBy.XPATH, xpaths["song_name"]))).text
        time_track = wait.until(selEc.presence_of_element_located((selBy.XPATH, xpaths["time_track"]))).text
        print(" * Played {0} for {1}".format(song_name, time_track))
        skip_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["skip_btn"])))
        skip_btn.click()


def init():
    print(r"""
      _____             _   _ _____       ____        _     __   ___  
     / ____|           | | (_)  __ \     |  _ \      | |   /_ | / _ \ 
    | (___  _ __   ___ | |_ _| |__) |   _| |_) | ___ | |_   | || | | |
     \___ \| '_ \ / _ \| __| |  ___/ | | |  _ < / _ \| __|  | || | | |
     ____) | |_) | (_) | |_| | |   | |_| | |_) | (_) | |_   | || |_| |
    |_____/| .__/ \___/ \__|_|_|    \__, |____/ \___/ \__|  |_(_)___/ 
           | |                       __/ |                            
           |_|                      |___/""")

    print("\n * Bot started.")
    selUrl = input(" * Insert Spotify playlist url (empty for default): ")
    headless = "--headless" in sys.argv
    with open('data/profiles.json', 'r') as f:
        credentials = json.load(f)
        print(" * Opening browsers...")
        for data in credentials['credentials']:
            threading.Thread(target=run, args=[data['username'], data['password'], selUrl, headless]).start()
            time.sleep(1)
        f.close()


if __name__ == '__main__':
    init()
# script modified by thisisawesome1994