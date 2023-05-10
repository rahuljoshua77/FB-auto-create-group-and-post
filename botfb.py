from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time,os,base64,json,csv,re
from selenium import webdriver
import warnings,io
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from time import sleep
cwd = os.getcwd()
opts = Options()
import pandas as pd

# opts.add_argument('--headless=chrome')
# #pts.headless = False
opts.add_argument('log-level=3') 
prefs = {"profile.default_content_setting_values.notifications" : 2}
opts.add_experimental_option("prefs",prefs)

dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
opts.add_argument('--ignore-certificate-errors')
import os

opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])

def date_show():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def xpath_fast(el):
    element_all = wait(browser,5).until(EC.presence_of_element_located((By.XPATH, el)))
    element_all.click()

def xpath_long(el):
    element_all = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, el)))
    return element_all.click()

 

def xpath_sel(el):
    element_all = wait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, el)))
    return element_all.click()

def xpath_type(el,text):
    wait(browser,30).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(text)
    
    

def login_acc():
 
    print()
    xpath_type('//*[@id="email"]',user)
    xpath_type('//*[@type="password"]',password)
    xpath_type('//*[@type="password"]',Keys.ENTER)
    sleep(10)
    cookies = browser.get_cookies()
    if os.path.exists(f'{cwd}/cookies') == False:
        os.mkdir(f'{cwd}/cookies')
    with open(f'{cwd}\\cookies\\{user}.json', 'w', newline='') as outputdata:
        json.dump(cookies, outputdata)
    
def main(data_file):
    global user,password 
    df = pd.read_excel(f"{cwd}//data/{data_file}")
    try:
        user = str(int(df.iloc[0, 0]))
    except:
        user = str(df.iloc[0, 0])
    password = df.iloc[0, 1]
    global browser
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=opts, desired_capabilities=dc)
    browser.get("https://www.facebook.com/")
    if not os.path.exists(f"{cwd}//cookies"):
        os.makedirs(f"{cwd}//cookies")
        
    try:
        with open(f"{cwd}//cookies//{user}.json", 'r') as cookiesfile:
            cookies = json.load(cookiesfile)
        for cookie in cookies:
            browser.add_cookie(cookie)
        login_success = "True"
    except:
        try:
            login_acc()
            print(f"{date_show()} [{user}] Success login")
            login_success = "True"
        except Exception as e:
            login_success = "False"
    
    if login_success == "True":
        browser.get("https://www.facebook.com/?ref=logo")
        xpath_long('//*[@aria-label="Profil Anda"]')
        print(f"{date_show()} [{user}] Change to fanspage")
        xpath_long('//*[@aria-label="Beralih Profil"]')
        sleep(5)
        print(f"{date_show()} [{user}] Change succes")
        for index, row in df.iterrows():
            nama_grup = row['Group Name']
            background_grup = row['Group Background']
            deskripsi_grup = row['Group Description']
            postingan_grup = row['Status']
            post_photo = row['Photo Post']
             
            browser.get('https://www.facebook.com/groups/create/')
            print(f"{date_show()} [{user}] Trying to create group {nama_grup}")
            xpath_type('//input[@type="text"]',nama_grup)
            print(f"{date_show()} [{user}] Input name group")
            xpath_long('//label[@aria-haspopup="listbox"]')
            xpath_long('(//div[@role="option"])[1]')
            sleep(2)
            xpath_long('//*[@aria-label="Formulir Pembuatan Grup"]//div[@aria-label="Buat"]')
            print(f"{date_show()} [{user}] Creating group")
            xpath_long('//div[@aria-label="Edit foto sampul grup"]')
            xpath_type('(//input[@type="file"])[1]',background_grup)
            sleep(2)
            browser.execute_script('window.scrollTo(0, 0);') 
            sleep(1)
            xpath_long('(//div[@aria-label="Simpan perubahan"])[2]')
            
            print(f"{date_show()} [{user}] Success create grup")
            browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            sleep(2)
            xpath_long('//span[text()="Tulis sesuatu..."]')
            print(f"{date_show()} [{user}] Update status")
            #xpath_long('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/divs')
            try:
                if "jpg" in post_photo.lower() or "png" in post_photo.lower():
                    xpath_type('//div[@id="toolbarLabel"]/parent::div//input[@type="file"]',post_photo)
            except:
                pass       
            if r"\n" in str(postingan_grup):
                for i in str(postingan_grup).split("\\n"):
                    xpath_type('//*[@aria-label="Buat postingan publik..."]',i)
                    sleep(0.5)
                    xpath_type('//*[@aria-label="Buat postingan publik..."]',Keys.SHIFT + Keys.ENTER)
            else:
                xpath_type('//*[@aria-label="Buat postingan publik..."]',postingan_grup)
                #xpath_type('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div',Keys.ENTER)
            
            xpath_long('//div[@aria-label="Posting"]')
            print(f"{date_show()} [{user}] Success update status")
            sleep(1)
            try:
                element_all = wait(browser,5).until(EC.presence_of_element_located((By.XPATH, '//div[@data-ad-comet-preview="message"]')))
                browser.execute_script("arguments[0].scrollIntoView();", element_all)
            except:
                pass
            xpath_long('(//div[@aria-label="Suka"])[1]')
            
            sleep(1)
            try:
                xpath_fast("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div/div[4]/div[3]/div")
            except:
                xpath_fast('/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div/div[4]/div[3]/div')
            if "\n" in deskripsi_grup:
                for i in deskripsi_grup.split("\n"):
                    xpath_type('//label[@aria-label="Keterangan"]//textarea',i)
                    sleep(0.5)
                    xpath_type('//label[@aria-label="Keterangan"]//textarea',Keys.ENTER)
            else:
                xpath_type('//label[@aria-label="Keterangan"]//textarea',deskripsi_grup)
            xpath_long('//div[@aria-label="Simpan"]')
            sleep(4)
            
            print(f"{date_show()} [{user}] Success like status")
            sleep(5)

    if login_success == "False":
        print(f"{date_show()} [{user}] Failed login")

if __name__ == '__main__':
    print(f'{date_show()} FB Auto Create Group')
    jumlah = int(input(f"{date_show()} Multi Chrome: "))
    file_list = "info.txt"
    list_accountsplit = os.listdir(f"{cwd}//data")
 
    with Pool(jumlah) as p:  
        p.map(main, list_accountsplit)