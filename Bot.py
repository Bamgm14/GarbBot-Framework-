from selenium.webdriver.common.keys import Keys
from selenium.webdriver import *
import time as t
import os,json,asyncio,logging
import Core as c
from Modules import Test
import sqlite3 as sql

class Bot(c.API):
    def __init__(self,bot_name,command_prefix,browser,profile_file,log,headless=False,db="Users.sql"):
        super().__init__(browser,profile_file,log,headless)
        self.message = None
        self.bot_name = bot_name.lower()
        self.command_prefix = command_prefix.lower()
        self.commands = {"help": {"desc": "This is the help function","func": lambda bot: bot.typer(self.__help_command__(), bot.textbox)},
                         "bye": {"desc": "Removes bot from specific chat", "func": lambda bot: bot.typer(self.__remove_user__(),bot.textbox)},}
        #Commands must have the command, description and function it reference
        self.con = sql.connect(db)
        self.users = {}
        con = self.con.cursor()
        con.execute("create table if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT, name char(128),login int,last_login int, last_logout int)")
        self.con.commit()
        self.__get_user__()

    def __get_user__(self):
        con = self.con.cursor()
        con.execute('select name,login from users')
        for x in con.fetchall():
            self.users[x[0]] = x[1]
            
    def __add_user__(self):
        con = self.con.cursor()
        if self.username not in self.users.keys():
            con.execute("insert into users(name,login,last_login) values(?,?,?)",(self.username,1,int(t.time())))
            ret = f"Hello, This is {self.bot_name}, Thank You For Calling Me, {self.username}. If you need help, Say {self.command_prefix}help\nIf you want me to leave say {self.command_prefix}bye.\n"
        else:
            if not self.users[self.username]:
                con.execute("update users set login = ?,last_login = ? where name = ?",(1,int(t.time()),self.username))
                ret = f"Hello, This is {self.bot_name}, Thank You For Calling Me Again, {self.username}. If you need help, Say {self.command_prefix}help\nIf you want me to leave say {self.command_prefix}bye.\n"
            else:
                ret = 'I am already here\n'
        self.con.commit()
        self.__get_user__()
        return ret
        
    def __remove_user__(self):
        con = self.con.cursor()
        con.execute("update users set login = ?,last_logout = ? where name = ?",(0,int(t.time()),self.username))
        self.con.commit()
        self.__get_user__()
        return "Goodbye!\n"
        
    def __get_new_msg__(self):
        try:
            self.register = self.driver.find_elements_by_class_name(self._classes_["greendot"])
            if len(self.register) > 0:
                ele = self.register[-1]
                action = ActionChains(self.driver)
                action.move_to_element_with_offset(ele, 0, -30)
                try:
                    action.perform()
                    action.click()
                    action.perform()
                    action.click()
                    
                except Exception as e:
                    pass
        except InvalidSessionIdException as e:
            self.log.error(e)
            raise c.BotException(f"The Browser has an error.\n{str(e)}")
        except Exception as e:
            self.log.warning(e)
            
    def add_command(self,command_name,desc,function):
        self.commands[command_name.lower()] = {"desc": desc,"func": function}
        
    def remove_command(self,command_name):
        del self.commands[command_name.lower()]
        
    def add_commands(self,dct):
        for x in dct.keys():
            try:
                self.add_command(x,*dct[x].values())
            except:
                self.add_command(x,*dct[x])
                
    def remove_commands(self,lst):
        for x in lst:
            self.remove_command(x)
            
    def __help_command__(self):
        hlp = '*[Help]*\n'
        for x in self.commands.keys():
            hlp += self.command_prefix + x + ":" + self.commands[x]["desc"] + "\n"
        return hlp[:-1]
        
    def start(self):
        while self.message != self.command_prefix + "killswitch":
            try:
                self.__get_new_msg__()
                try:
                    self.driver.find_element_by_xpath(self._xpaths_["down"]).click()
                except:
                    pass
                try:
                    try:
                        self.driver.find_elements_by_class_name(self._classes_["message"])[-1]
                    except:
                        continue
                    if self.message == self.driver.find_elements_by_class_name(self._classes_["message"])[-1].text:
                        continue
                    self.username = self.driver.find_element_by_xpath(self._xpaths_["name"]).text
                    self.message = self.driver.find_elements_by_class_name(self._classes_["message"])[-1].text
                    self.textbox = self.chat_textbox()
                    self.log.info(f"Name:{self.username}")
                    self.log.info(f"Message:{self.message}")
                    if self.command_prefix == self.message.split(' ')[0].lower()[0]:
                        if self.message.split(' ')[0].lower()[1:] == self.bot_name:
                            self.typer(self.__add_user__(),self.textbox)
                            continue
                        if self.users[self.username] and self.message.split(' ')[0].lower()[1:] in self.commands.keys():
                            self.commands[self.message.split(' ')[0].lower()[1:]]["func"](self)
                            continue
                except Exception as e:
                    self.log.warning(e)
            except c.BotException as e:
                self.log.critical(e)
                break
            except Exception as e:
                self.log.error(e)
                self.driver.refresh()
        self.close()
        
if __name__ == '__main__':
    bot_name = input("Bot Name:")
    command_prefix = input("Command Prefix:")
    browser = input("Browser Name:")
    profile_file = input("File name for WhatsApp Profile:")
    log_level = input("Enter log level:")
    garb = Bot(bot_name,command_prefix,browser,profile_file,log_level,)
    garb.add_commands({"test_image": ["Image Test Run",Test.test_picture],"test_text":["Text Test Run",Test.test_text]})
    garb.start()