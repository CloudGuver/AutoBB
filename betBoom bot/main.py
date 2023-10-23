from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from undetected_chromedriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from fake_useragent import UserAgent
from time import sleep
import os



ua = UserAgent(fallback='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')

op = Options() 
#op.add_argument(ua.random)  
op.add_argument('--no-first-run --no-service-autorun --password-store=basic')
op.add_argument(f'--user-data-dir={os.getcwd()}\\BB\\test')
#op.add_argument('--mute-audio')
#
# op.add_argument('--disable-notification')

#capa = DesiredCapabilities.CHROME
#capa["pageLoadStrategy"] = "eager"
#capa["pageLoadStrategy"] = "none"

driver = Chrome(options=op,
                use_subprocess=True,
                #desired_capabilities=capa,
                version_main=118)

driver.get('https://betboom.ru/sport')
#driver.save_screenshot('nowsecure.png')
input()
#sleep(10)