import datetime as d
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time as t
import User as u
import Modules.Constant as c
import Commands as cmd
import os
hlp=open('Help.txt','r').read()
driver = webdriver.Firefox()
driver.maximize_window()
driver.get('http://web.whatsapp.com')
page=driver.page_source
print('Please Scan the QR Code')
while page==driver.page_source:
    pass
while True:
    try:
        user=u.Users()
        register=driver.find_elements_by_class_name(c.Greendot)
        date=d.datetime.now().isoformat()
        try:
            driver.find_element_by_xpath(c.Down).click()
        except:
            pass
        if len(register) > 0:
            ele = register[-1]
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(ele, 0, -20)
            try:
                action.click()
                action.perform()
                action.click()
                action.perform()
            except Exception as e:
                pass
            try:
                name = driver.find_element_by_xpath(c.Nme).text
                message = driver.find_elements_by_class_name(c.Msg)[-1].text.lower()
                time = message.split('\n')[len(message.split('\n'))-1]
                if len(message.split('\n'))>=3:
                    UserName=message.split('\n')[len(message.split('\n'))-3]
                else:
                    UserName=name
                #UserName=driver.find_elements_by_class_name(c.Info)[-1].get_attribute('data-pre-plain-text').split("]")[1].replace(':','').replace(' ','')
                message=message.split('\n')[len(message.split('\n'))-2]
                a=open('MessageHistory.txt','a')
                a.write('{"'+name+'":("'+UserName+'","'+message+'","'+time+'")}\n====\n')
                a.close()
                textbox = driver.find_element_by_xpath(c.Tbx)
                if 'garbage.exe' in message.lower():
                    if name not in user:
                        u.ArriveUser(name,date)
                        response='Hello, This Is Garbage, Thank You For Calling Me, '+name+'. If you need help, Say !help, If you want me to leave say bye garb and please no enter keys(\\n)\n'
                        textbox.send_keys(response)
                        pass
                    elif name in user and 'false' in user[name].lower():
                        u.ArriveUser(name,date)
                        response='Hello, This Is Garbage, Thank You For Calling Me Again, '+name+'. If you need help, Say !help, If you want me to leave say bye garb and please no enter keys(\\n)\n'
                        textbox.send_keys(response)
                        pass
                    else:
                        response='I am already here\n'
                        textbox.send_keys(response)
                        pass
                if (name in user) and ('true' in user[name].lower()):
                    if '!help' in message:
                        res=hlp
                        for x in res.split('\n'):
                            textbox.send_keys(x)
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                        textbox.send_keys('\n')
                    if 'bye garb' in message.lower():
                        response='Goodbye\n'
                        textbox.send_keys(response)
                        u.LeaveUser(name,date)
                        continue
                    if '!killswitch' in message.lower():
                        break
                    cmd.Commands(driver,textbox,date,message,name,UserName)
            except Exception as e:
                try:
                    driver.find_element_by_class_name(c.Qt).click()
                except:
                    pass
                print(e)
                if 'Message' not in str(e):
                    if (name in user) and ('true' in user[name].lower()):
                        textbox = driver.find_element_by_xpath(c.Tbx)
                        response=str(e)[0].upper()+str(e)[1:]+'\n'
                        textbox.send_keys(response)
                        print (e)
            t.sleep(1)
    except Exception as e:
        driver.get('http://web.whatsapp.com')
        print(e)
