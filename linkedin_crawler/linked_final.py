import os
import time
from selenium import webdriver
# from json_wr import read_status_json,write_status
# from  import write_status,read_status_json
from linkedin_crawler.json_wr  import read_status_json, write_status

driver_folder = os.path.join(os.getcwd(), "geckodriver-v0.24.0-win64")
DRIVER = os.path.join(driver_folder, 'geckodriver.exe')

def initial_setup(event_name):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
    driver = webdriver.Firefox(
        executable_path=DRIVER, firefox_profile=profile)
    return driver

def withdraw(driver):
    driver.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')
    time.sleep(10)
    print("network might be there it must be ok to continue")
    print("vesrt ")
    i = 0
    try :
        while i < 100:
            w_btd2 = driver.find_element_by_xpath(
                '/html/body/div[8]/div[3]/div/div/div/div/div/div/section/div/div[2]/ul/li[1]/div/div[2]/button')
            w_btd2.click()
            time.sleep(2)
            wc = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
            wc.click()
            i += 1
            time.sleep(2)
            print(i)
    except Exception as e :
        print(i)

def scrool_page_end(start):
    t = 0
    while t==0:
        try:
            test = driver.find_element_by_xpath(
                '/html/body/div[8]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[{}]/div[2]/div[1]/button'.format(
                    start))
            t = 1

        except Exception as e:
            print("scrooling down ")
            from selenium.webdriver.common.keys import Keys
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(10)

def msg_send(driver):
    data = read_status_json()

    start = data['request_end_no'] + 1
    end_t = input("enter end no to sends ")
    end = data['request_end_no'] + int(end_t)
    scrool_page_end(start)
    total_newly_msged = 0
    totak_sent = data['totak_sent']
    total_previously_msged = data['total_previously_msged']
    total_newly_msged = data['total_newly_msged']

    for i in range(start,end,1):
        # '/html/body/div[8]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[{}]/div[2]/div[1]/button'
        # '/html/body/div[8]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[{}]/div/div[2]/div[1]/button'
        element_id = i
        data['request_end_no'] +=1
        test = driver.find_element_by_xpath(
        '/html/body/div[8]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[{}]/div[2]/div[1]/button'.format(
            element_id))
        test.click()
        time.sleep(3)
        print('selected use')

        try:
            msg_box = driver.find_element_by_xpath(
                '/html/body/div[8]/aside/div[2]/div[1]/form/div[2]/div/div[1]/div[1]')
            msg_box.send_keys('Hi can you endorse me for MySQL much appreciated.Thanks  ')
            time.sleep(3)
            send_btn = driver.find_element_by_xpath(
                '/html/body/div[8]/aside/div[2]/div[1]/form/footer/div[2]/div[1]/button')
            send_btn.click()
            print('Send msg')
            data['total_newly_msged'] += 1
        except Exception as e:
            data['total_previously_msged'] += 1
            print('previously msged ')
            write_status(data)

        time.sleep(3)
        try:
            close_key = driver.find_element_by_xpath('/html/body/div[8]/aside/div[2]/header/section[2]/button[2]')
            close_key.click()
            write_status(data)
        except Exception as e:
            close_key = driver.find_element_by_xpath('/html/body/div[8]/aside/div[2]/header/section[2]/button[2]/li-icon/svg')
            close_key.click()
            write_status(data)
        print('closed ')
        time.sleep(3)
        print("message sent to id :  ",element_id)
        write_status(data)

    write_status(data)

def choice(driver):
    while True:
        print("Make sure you have logged in : choose: 1)quit 2)withdraw 3)send msg 4)send connetction\n ",end="\r")
        choice = input()
        choice = int(choice)
        if choice == 1:
            print("quit ")
            # driver.close()
            driver.quit()
            break
        elif choice == 2:
            print("withdraw ")
            withdraw(driver)
        elif choice == 3:
            print("send msg ")
            try:
                msg_send(driver)
            except Exception as e:
                print(e )
        elif choice == 4:
            print("send connection ")
        else:
            print("enter a valid option ")

def ex():
    pass

if __name__ == '__main__':
    print("PGM started please enter login details")
    driver = initial_setup(0)
    driver.get('https://www.linkedin.com/')
    choice(driver)
    print("extited the program logout and close ")

"""
LIMITS : 
1) Invitations / connection requests —100 / day
2) Messages to 1st connections — 150 / day
3) Messages to group members — 15 / month per all LinkedIn groups
4) Endorsements — 60 /day
5) Profile Extractor — 150 / day
6) Profile Auto-Visiting —150 / day
7) Profile Auto-Follower — 150 / day
8) Collect from search (for inviting, messaging, exports or auto-visiting) — 2000 contacts / day

SPLIT : 
Monday : 100 invites
Tuesday : 150 messages
Wednesday : 60 endorsements
"""
