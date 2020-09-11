from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as selEc
from selenium.webdriver.common.by import By as selBy
from selenium.webdriver.support.ui import WebDriverWait
import json, time, threading, random, sys
from modules.spotify import links, xpaths

from sys import stdout
from requests import post
from os import system, _exit, path
from random import choice, randint
from colors import green, red, reset
from time import time, sleep, strftime, gmtime
from threading import Thread, Lock, active_count
from string import ascii_letters, ascii_lowercase, digits

system('cls && title [Spotify Account Creator] - Main Menu')
headers = {'User-agent': 'S4A/2.0.15 (com.spotify.s4a; build:201500080; iOS 13.4.0) Alamofire/4.9.0', 'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Accept': 'application/json, text/plain;q=0.2, */*;q=0.1', 'App-Platform': 'IOS', 'Spotify-App': 'S4A', 'Accept-Language': 'en-TZ;q=1.0', 'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5', 'Spotify-App-Version': '2.0.15'}
domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'hotmail.co.uk', 'hotmail.fr', 'outlook.com', 'icloud.com', 'mail.com', 'live.com', 'yahoo.it', 'yahoo.ca', 'yahoo.in', 'live.se', 'orange.fr', 'msn.com', 'mail.ru', 'mac.com']
lock = Lock()

class Main:
    def __init__(self):
        self.variables = {
            'proxies': [],
            'proxy_num': 0,
            'created': 0,
            'retries': 0,
            'cpm': 0,
            'unlimited': False
        }

        logo = '''                                            ____ ___  ____ ___ _ ____ _   _       
                                            [__  |__] |  |  |  | |___  \_/        
                                            ___] |    |__|  |  | |      |         
                                      ____ ____ _  _ ____ ____ ____ ___ ____ ____ 
                                      | __ |___ |\ | |___ |__/ |__|  |  |  | |__/ 
                                      |__] |___ | \| |___ |  \ |  |  |  |__| |  \ '''

        print('%s%s' % (green(), logo))

        print('\n\n %s[%s1%s] HTTP\n [%s2%s] SOCKS4\n [%s3%s] SOCKS5\n\n%s> %sSelect a Proxy Type%s: ' % (green(), reset(), green(), reset(), green(), reset(), green(), reset(), green(), reset()), end = '')
        self.proxy_type = '1'
        if self.proxy_type.upper() in ['1', 'HTTP']:
            self.proxy_type = 'http'
        elif self.proxy_type.upper() in ['2', 'SOCKS4']:
            self.proxy_type = 'socks4'
        elif self.proxy_type.upper() in ['3', 'SOCKS5']:
            self.proxy_type = 'socks5'
        else:
            print('\n%s> %sInvalid input%s.' % (reset(), red(), reset()))
            system('title [Spotify Account Creator] - Exiting . . .')
            sleep(3)
            _exit(0)

        print('%s> %sAmount to create (empty for unlimited)%s: ' % (reset(), green(), reset()), end = '')
        self.amount = '12'
        print()

        if self.amount == '':
            self.variables['unlimited'] = True
            self.amount = 0
        elif self.amount != '' and not self.amount.isdigit():
            print('%s> %sInvalid input%s.' % (reset(), red(), reset()))
            system('title [Spotify Account Creator] - Exiting . . .')
            sleep(3)
            _exit(0)

    def setup(self):
        if path.exists('Proxies.txt'):
            with open('Proxies.txt', 'r', encoding = 'UTF-8') as f:
                for line in f.read().splitlines():
                    if line != '':
                        self.variables['proxies'].append(line)
            if len(self.variables['proxies']) == 0:
                self.error_import(False)
        else:
            self.error_import(True)

    def error_import(self, create):
        if create:
            open('Proxies.txt', 'a').close()
        print('%s> %sPaste your proxies inside Proxies.txt%s!' % (reset(), red(), reset()))
        system('title [Spotify Account Creator] - Exiting . . .')
        sleep(3)
        _exit(0)

    def write(self, arg):
        lock.acquire()
        stdout.flush()
        stdout.write('%s\n' % (arg.encode('ascii', 'replace').decode())) # Get less printing bugs on Windows
        lock.release()

    def cpm_counter(self):
        if self.variables['unlimited']:
            while True:
                old = self.variables['created']
                sleep(4)
                new = self.variables['created']
                self.variables['cpm'] = ((new - old) * 15)
        else:
            while self.variables['created'] != int(self.amount):
                old = self.variables['created']
                sleep(4)
                new = self.variables['created']
                self.variables['cpm'] = ((new - old) * 15)

    def update_title(self):
        if self.variables['unlimited']:
            while True:
                elapsed = strftime('%H:%M:%S', gmtime(time() - self.start))
                system('title [Spotify Account Creator] - Created: %s ^| Retries: %s ^| CPM: %s ^| Time Elapsed: %s ^| Threads: %s' % (self.variables['created'], self.variables['retries'], self.variables['cpm'], elapsed, (active_count() - 2)))
                sleep(0.4)
        else:
            while self.variables['created'] != int(self.amount):
                elapsed = strftime('%H:%M:%S', gmtime(time() - self.start))
                system('title [Spotify Account Creator] - Created: %s/%s ^| Retries: %s ^| CPM: %s ^| Time Elapsed: %s ^| Threads: %s' % (self.variables['created'], self.amount, self.variables['retries'], self.variables['cpm'], elapsed, (active_count() - 2)))
                sleep(0.4)

            elapsed = strftime('%H:%M:%S', gmtime(time() - self.start))
            system('title [Spotify Account Creator] - Created: %s/%s ^| Retries: %s ^| CPM: %s ^| Time Elapsed: %s ^| Threads: %s' % (self.variables['created'], self.amount, self.variables['retries'], self.variables['cpm'], elapsed, (active_count() - 2)))

    def retry(self):
        self.variables['retries'] += 1
        self.creator(choice(self.variables['proxies']))

    def creator(self, proxy):
        email = '%s@%s' % (''.join(choice(ascii_lowercase + digits) for _ in range(randint(7, 10))), choice(domains))
        password = ''.join(choice(ascii_letters + digits) for _ in range(randint(8, 14)))
        birth_year = randint(1970, 2005)
        birth_month = randint(1, 12)
        birth_day = randint(1, 28)
        gender = choice(['male', 'female'])

        data = 'creation_point=lite_7e7cf598605d47caba394c628e2735a2&password_repeat=%s&platform=Android-ARM&iagree=true&password=%s&gender=%s&key=a2d4b979dc624757b4fb47de483f3505&birth_day=%s&birth_month=%s&email=%s&birth_year=%s' % (password, password, gender, birth_day, birth_month, email, birth_year)
        
        try:
            create = post('https://spclient.wg.spotify.com/signup/public/v1/account', data = data, headers = headers, proxies = {'https': '%s://%s' % (self.proxy_type, proxy)}, timeout = 5)
            if create.json()['status'] == 1:
                username = create.json()['username']
                if username != '':
                    self.write('%s[%sCREATED%s] %s:%s | Username: %s | Gender: %s | Date of Birth: %s/%s-%s' % (green(), reset(), green(), email, password, username, gender.replace(gender[0], gender[0].upper()), birth_day, birth_month, birth_year))
                    with open('credentials.txt', 'a', encoding = 'UTF-8') as f: f.write('%s:%s\n' % (email, password))
                    with open('Created [CAPTURE].txt', 'a', encoding = 'UTF-8') as f: f.write('%s:%s | Username: %s | Gender: %s | Date of Birth: %s/%s-%s\n' % (email, password, username, gender.replace(gender[0], gender[0].upper()), birth_day, birth_month, birth_year))

                    self.variables['created'] += 1
                else:
                    self.retry()
            else:
                self.retry()
        except:
            self.retry()

    def multi_threading(self):
        self.start = time()
        Thread(target = self.cpm_counter).start()
        Thread(target = self.update_title).start()

        if self.variables['unlimited']:
            while True:
                try:
                    Thread(target = self.creator, args = (self.variables['proxies'][self.variables['proxy_num']],)).start()
                except:
                    continue
                self.variables['proxy_num'] += 1
                if self.variables['proxy_num'] >= len(self.variables['proxies']):
                    self.variables['proxy_num'] = 0
        else:
            num = 0
            while num < int(self.amount):
                try:
                    Thread(target = self.creator, args = (self.variables['proxies'][self.variables['proxy_num']],)).start()
                except:
                    continue
                num += 1
                self.variables['proxy_num'] += 1
                if self.variables['proxy_num'] >= len(self.variables['proxies']):
                    self.variables['proxy_num'] = 0
            
            while self.variables['created'] != int(self.amount):
                continue
            print('\n%s> %sFinished%s.' % (reset(), green(), reset()))

if __name__ == '__main__':
    main = Main()
    main.setup()
    main.multi_threading()


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

def run(username, password):

    # Open Chrome and head to playlist link
    
    proxy1 = random.choice(open('proxies.txt').readlines())
    useragent = random.choice(open('useragents.txt').readlines())
    opts1 = Options()
    opts1.add_argument('--user-agent=%s'% useragent)
    opts1.add_argument('--proxy-server=%s'% proxy1)
    #opts1.add_argument('--mute-audio')
    opts1.add_argument('--incognito')
    #opts1.add_argument('--headless')
    opts1.add_argument('--start-maximized')
    browser = webdriver.Chrome(executable_path='drivers/chromedriver.exe', options=opts1)
    wait = WebDriverWait(browser, 35)
    browser.get('redirect link here')
    
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
    selUrl = 'redirect link here'
    #with open('data/profiles.json', 'r') as f:
    #    credentials = json.load(f)
    #    print(" * Opening browsers...")
    #    for data in credentials['credentials']:
    #        threading.Thread(target=run, args=[data['username'], data['password']]).start()
    #        time.sleep(1)
    #    f.close()
    with open('credentials.txt') as f:
        credentials = [x.strip().split(':', 1) for x in f]
        print(" * Opening browsers...")
        for username, password in credentials:
            threading.Thread(target=run, args=[username, password]).start()
        f.close()


if __name__ == '__main__':
    init()
# script modified by thisisawesome1994