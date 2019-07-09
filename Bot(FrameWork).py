import datetime as d
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time as t
import User as u
import Modules.Constant as c
import Commands as cmd
import os
import md5
md5.Setup()
hlp=open('Help.txt','r').read()
driver = webdriver.Firefox()
driver.maximize_window()
driver.get('http://web.whatsapp.com')
print('Please Scan the QR Code')
while True:
    try:
        md5.Update()
    except:
        os.system('python3 Bot.py')
        break
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
                UserName=driver.find_element_by_xpath(c.Info).get_attribute('data-pre-plain-text').split("]")[1]
                a=open('MessageHistory.txt','a')
                a.write(name+'\n'+UserName+':'+message+'\n')
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
                    assert '\n' in message, 'Please No \\n(Enter Key)'
                    if '!help' in message:
                        res=hlp
                        for x in res.split('\n'):
                            textbox.send_keys(x)
                            textbox.send_keys(Keys.SHIFT+Keys.ENTER)
                        textbox.send_keys('\n')
                    cmd.Commands(driver,textbox,date,message,name,UserName)
                    if 'bye garb' in message.lower():
                        response='Goodbye\n'
                        textbox.send_keys(response)
                        u.LeaveUser(name,date)
                        pass
                    if 'killswitch' in message.lower():
                        break
            except Exception as e:
                print (e)
                try:
                    driver.find_element_by_class_name(c.Qt).click()
                except:
                    pass
                if 'Message' not in str(e):
                    if (name in user) and ('true' in user[name].lower()):
                        textbox = driver.find_element_by_xpath(c.Tbx)
                        response=str(e)[0].upper()+str(e)[1:]+'\n'
                        textbox.send_keys(response)
            t.sleep(1)
    except Exception as e:
        print(e)
