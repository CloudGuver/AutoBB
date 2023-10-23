from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumwire.undetected_chromedriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from googletrans import Translator
from twocaptcha import TwoCaptcha
from multiprocessing import Pool
from datetime import datetime
from random import randint
from time import sleep
from PIL import Image 
import warnings
import base64
import re
import os

ua = UserAgent(fallback='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
warnings.filterwarnings("ignore", category=DeprecationWarning)


class SEO:
    def __init__(self,auth_data):

        email,password = auth_data.split(';')
        
        
        op = Options() 
        op.add_argument(ua.random)  
        op.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        op.add_argument('--mute-audio')
        op.add_argument('--disable-notification')
        #op.add_argument('--headless=False')
        #op.add_argument(f'--user-data-dir={os.getcwd()}\\seo\\{email}')
        
        capa = DesiredCapabilities.CHROME
        #capa["pageLoadStrategy"] = "eager"
        capa["pageLoadStrategy"] = "none"
        
        self.driver = Chrome(options=op,
                            use_subprocess=True,
                            desired_capabilities=capa,
                            version_main=118)
        
        self.driver.implicitly_wait(20)       

        self.email = email
        self.password = password
        conf = {
                'server':           'api.captcha.guru',
                'apiKey':           '69eec54daf654a6773f93dceeacac393',
                'softId':            23425323523,
                'defaultTimeout':    120,
                'recaptchaTimeout':  600,
                'pollingInterval':   10,
                }
        self.recap = TwoCaptcha(**conf)
        config = {
            'server':           'rucaptcha.com',
            'apiKey':           '947ce2d26e57bb6492133bd156049153',
            'softId':            23425323523,
            'defaultTimeout':    120,
            'recaptchaTimeout':  600,
            'pollingInterval':   10,
            }
        self.clickcap = TwoCaptcha(**config)
        
    def time(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")
        

    def captcha(self):
        translator = Translator()
        print(f'[{self.time()}] Решаю каптчу. ')
        driver = self.driver

        if driver.find_elements(By.ID, 'capcha'):
            solver = self.clickcap
            elems = driver.find_elements(By.CLASS_NAME, 'out-capcha-lab')
            cap = Image.new('RGB', (80*len(elems),80))
            for i,elem in enumerate(elems):
                
                img_data = elem.get_attribute('style').split('base64,')[1].encode()
                with open("img.png", "wb") as f:
                    f.write(base64.decodebytes(img_data))
                img = Image.open('img.png')
                cap.paste(img, (80*i,0))

            task = driver.find_element(By.ID, 'capcha').text.split('\n')[0]
            task = translator.translate(task).text
            cap.save('img.png')
            try:
                #print(task)
                result = solver.coordinates(file = 'img.png', textinstructions = task)
                

                for i in result['code'].split(';'):
                    print(f'[{self.time()}] Кликаю по картинке.')
                    code = int(i.split('x=')[1].split(',')[0])//80
                    #print(code)
                    elems[code].click()

            except Exception as ex:
                print(ex)
                

            
        
        elif driver.find_elements(By.ID, 'captcha_new'):
            solver = self.recap
            try:
                driver.find_element(By.ID, 'captcha_new').screenshot('img.png')
                result = solver.normal(file='img.png',numeric=1,max_len=3)
                print(result)
                driver.find_element(By.ID,'code').send_keys(result['code'])
                print(f'[{self.time()}] Получил решение.')
                
            except Exception as ex:
                print(ex)
                

        elif driver.find_elements(By.CLASS_NAME,'g-recaptcha'):
            solver = self.recap
            try:
                
                
                answer = solver.recaptcha(sitekey='6Ldov_8SAAAAADdIZyGbKSxRZAgTzq-WMp11Bp4R',url='https://seo-fast.ru/')
                code = answer['code']
                print(f'[{self.time()}] Получил решение.')
                driver.execute_script('document.querySelector("[name=g-recaptcha-response]").innerHTML = ' + "'" + code + "'")
                sleep(2)
                    
            except Exception as ex:
                    print(ex)
                    

        else:
            return

        driver.find_element(By.CLASS_NAME,'sf_button').click()
        
        
        
        print(f'[{self.time()}] Решил каптчу. ')
        try:
            print(result)
            
            return result
        except Exception as ex:
                    print(ex)
                    pass

    def get_bonus(self):
        driver = self.driver
        bonus = int(driver.find_element(By.ID, 'actions_bonus').text())
        if bonus > 99:
            driver.find_element(By.CLASS_NAME, 'sf_button_orange').click()

        print(f'[{self.time()}] Собрал бонус в размре {bonus} очков. ')
        

    def login(self):
        driver = self.driver
        driver.get('https://seo-fast.ru/login')
        sleep(5)
        if re.search('Регистрация',driver.find_element(By.CLASS_NAME, 'regbutton').text):
           
            try:
                driver.find_element(By.ID,'logusername').send_keys(self.email)
                print(f'[{self.time()}] Авторизуюсь...')
                sleep(1)
                driver.find_element(By.ID,'logpassword').send_keys(self.password)
                sleep(1)
                try:
                    driver.find_element(By.XPATH,'//*[@id="restorepassgo"]/form/center/div[1]/span/input[1]').click()
                except:
                    pass
                result = self.captcha()
                

            except Exception as ex:
                print(ex)
                pass
            
            for _ in range(10):
                sleep(1.5)
                if re.search('mystat',driver.current_url):
                    break
                
                    
            else:
                print(f'[{self.time()}] Ошибка при авторизации.')
                try:
                    self.clickcap.report(result['captchaId'], False)
                    print(f'[{self.time()}] Отправил репорт')
                except:
                    pass
                sleep(1.5)
                self.login()

        print(f'[{self.time()}][{self.email}] => Authorization successful. ')
        
    def close_warning(self):
        driver = self.driver
        if driver.find_elements(By.CLASS_NAME,'popup2-content'):
            print(f'[{self.time()}] Закрываю предупреждение.')
            sleep(1)
            driver.find_element(By.CSS_SELECTOR,'#window_popup2 > div > a').click()
            sleep(1)
            driver.find_element(By.CSS_SELECTOR,'#window_popup3 > div > a').click()         

    def check_info(self):
        driver = self.driver
        print(f'[{self.time()}] Выполняю условие для доступа к просмотрам.')
        if driver.find_elements(By.CLASS_NAME,'info'):
            
            if re.search('Перейдите в раздел "Задания"',driver.find_element(By.CLASS_NAME,'info').text):
                print(f'[{self.time()}] Перехожу в раздел заданий')
                driver.find_element(By.CLASS_NAME,'sf_button').click()
                sleep(3)
                try:
                    self.close_warning()
                except Exception as ex:
                    print(ex)
                    
                sleep(1)
                url = 'https://seo-fast.ru//work_task?read&adv=' + driver.find_element(By.ID,'load_page_all').find_element(By.TAG_NAME,'tr').get_attribute('id').replace('task_nov','')
                driver.get(url)
                sleep(2)
                driver.get('https://seo-fast.ru/work_youtube')
                
    def start_work(self):
        driver = self.driver
        driver.implicitly_wait(20)
        
        driver.get('https://seo-fast.ru/work_youtube')
        self.check_info()
        
        sleep(1)
        if driver.find_elements(By.CLASS_NAME,'popup2-content'):
            print(f'[{self.time()}] Закрываю предупреждение перед просмотром.')
            sleep(1)
            driver.find_element(By.CLASS_NAME,'sf_button').click()

            
    def worker(self, url):
        driver = self.driver
        try:
            self.start_work()
        except Exception as ex:
            print(ex)
        print(f'[{self.time()}] Начал просмотр.')
        driver.get(url)
        count = 0
        error = 0
        views = len(driver.find_elements(By.CLASS_NAME, 'youtube_v'))
        print(f'[{self.time()}] Доступно к просмотру:',views)
        
        for i in range(1,views):

            try:
                driver.implicitly_wait(2)
                if driver.find_elements(By.CLASS_NAME,'info'):
                    
                    self.worker(url)
                if driver.find_elements(By.ID, 'captcha_new'):
                    print(f'[{self.time()}] Наткнулся на каптчу. ')
                    
                    self.worker(url)
                if int(datetime.now().strftime("%H")) == 23:
                    self.get_bonus()
                    
                ids = driver.find_elements(By.CLASS_NAME,'surf_ckick')[error].get_attribute('onclick').split("'")[1].split("'")[0]
                driver.set_page_load_timeout(20)
                driver.find_element(By.XPATH,f'//*[@id="res_views{ids}"]/div/a').click()
                sleep(2)
                
                    
                driver.switch_to.window(driver.window_handles[-1])
                driver.implicitly_wait(10)

                time = int(driver.find_element(By.ID,'tmr').text)
                sleep(3)
                frame = driver.find_element(By.ID,'video-start')
                driver.switch_to.frame(frame)
                
                if not driver.find_elements(By.CLASS_NAME,'ytp-error-content-wrap-reason'):

                    driver.find_element_by_class_name('ytp-large-play-button').click()
                    print(f'[{self.time()}] Ждать осталось {time} секунд. ')
                    sleep(time+randint(2,4))
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME,'sf_button').click()

                    for _ in range(10):
                        if re.search('Просмотр засчитан',driver.find_element(By.ID,'succes-error').text):

                            driver.switch_to.window(driver.window_handles[0])
                            count+=1
                            print(f'[{self.time()}] Задание № {count}',driver.find_element(By.ID,'succes-error').text)#driver.find_element(By.ID,f'res_views{ids}').text)
                            break
                        sleep(1)
                else:
                    error+=2

        
                
            except Exception as ex:
                #print(ex)
                
                for i in range(1,len(driver.window_handles)):
                    driver.switch_to.window(driver.window_handles[i])
                    driver.close()
                    
                driver.switch_to.window(driver.window_handles[0])

            else:
            
                for i in range(1,len(driver.window_handles)):
                    driver.switch_to.window(driver.window_handles[i])
                    driver.close()
                    
                driver.switch_to.window(driver.window_handles[0])
                
        else:
            if driver.find_elements(By.CLASS_NAME,'info'):
                self.worker(url)

    def close_driver(self):
        self.driver.close()
        self.driver.quit()    


def main():
    bot = SEO(auth_data = 'chgtolik@gmail.com;68264bdb65')
    
    try:
        bot.login()
        print(f'[{bot.time()}] Готовлюсь к работе...')
        #bot.start_work()
        bot.worker('https://seo-fast.ru/work_youtube?video_youtube')
        bot.worker('https://seo-fast.ru/work_youtube?expensive_youtube')
    except Exception as ex:
        print(ex)
        
    input()
    bot.close_driver()


if __name__ == '__main__':

    main()
