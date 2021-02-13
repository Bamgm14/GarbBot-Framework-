from selenium.webdriver.common.keys import Keys
from selenium.webdriver import *
from msedge.selenium_tools import *
import time as t
import os,json,asyncio,logging

class BotException(Exception):
    pass
class API:
    def __init__(self,browser,filename,log,headless=False):
        self._loglevel_ = {"info": 20,"debug": 10,
                           "warning": 30,"error": 40,
                           "critical": 50,"null": 0}
                           
        self._browsers_ = {"chrome": [Chrome, ChromeOptions],"firefox": [Firefox, FirefoxOptions], #Chrome is weird and doesn't work for some reason
                           "edge": [Edge, EdgeOptions],"opera": [Opera,lambda : self.__execute_error__(f"No Headless for {browser}")],
                           "safari": [Safari,lambda : self.__execute_error__(f"No Headless for {browser}")]}
                           
        self._xpaths_ = {"attachment": '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/div/span',
                         "send_file": '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span',
                         "attachment_type": '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input',
                         "caption": '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]',
                         "scroll": 'arguments[0].scrollIntoView();',
                         "name": '/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span',
                         "textbox": '/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]',
                         "down": '/html/body/div[1]/div/div/div[4]/div/div[3]/div/span[2]/div/span[2]',
                         "test": '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div',
                         "search_group": '/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]',
                         "searched_chat": '/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div[12]/div/div/div[2]/div[1]/div[1]/span/span',
                         "close": '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/header/div/div[1]/button'}
        
        self._classes_ = {"greendot": 'VOr2j',
                          "message": '_1wlJG',
                          "close": 'hYtwT'}

        self.log = logging.getLogger("Bot")        
        log_stream = logging.StreamHandler()
        log_file = logging.FileHandler('Bot.log')
        log_format = logging.Formatter('%(asctime)s [%(levelname)s] (%(funcName)s): %(message)s')
        log_stream.setFormatter(log_format)
        log_file.setFormatter(log_format)
        self.log.addHandler(log_stream)
        self.log.addHandler(log_file)
        self.change_log_level(log)
        
        if browser.lower() in self._browsers_.keys():
            if headless:
                options = self._browsers_[browser.lower()][1]()
                options.headless = headless
                self.driver = self._browsers_[browser.lower()][0](options = options)
            else:
                self.driver = self._browsers_[browser.lower()][0]()
        else:
            self.close()
            raise BotException("Browser Type Not Found.")
        self.driver.maximize_window()
        self.driver.get('http://web.whatsapp.com')
        if not os.path.isfile(filename):
            if headless:
                raise BotException("Cannot Run QR Scan which requires GUI.")
            print('Please Scan the QR Code')
            if 'y' == input("Do you want to save session for future loads?[Y/N]:")[0].lower():
                self.__save_profile__(self.__get_indexed_db__(),filename)
        else:
            self.__access_by_file__(filename)
    def __execute_error__(self,message):
        raise BotException(message)
        
    def __get_indexed_db__(self):
        #Code taken from WaWebSessionHandler-master by jeliebig
        self.log.debug('Executing getIDBObjects function...')
        self.driver.execute_script('window.waScript = {};'
                                     'window.waScript.waSession = undefined;'
                                     'function getAllObjects() {'
                                     'window.waScript.dbName = "wawc";'
                                     'window.waScript.osName = "user";'
                                     'window.waScript.db = undefined;'
                                     'window.waScript.transaction = undefined;'
                                     'window.waScript.objectStore = undefined;'
                                     'window.waScript.getAllRequest = undefined;'
                                     'window.waScript.request = indexedDB.open(window.waScript.dbName);'
                                     'window.waScript.request.onsuccess = function(event) {'
                                     'window.waScript.db = event.target.result;'
                                     'window.waScript.transaction = window.waScript.db.transaction('
                                     'window.waScript.osName);'
                                     'window.waScript.objectStore = window.waScript.transaction.objectStore('
                                     'window.waScript.osName);'
                                     'window.waScript.getAllRequest = window.waScript.objectStore.getAll();'
                                     'window.waScript.getAllRequest.onsuccess = function(getAllEvent) {'
                                     'window.waScript.waSession = getAllEvent.target.result;'
                                     '};'
                                     '};'
                                     '}'
                                     'getAllObjects();')
        self.log.debug('Waiting until IDB operation finished...')
        while not self.driver.execute_script('return window.waScript.waSession != undefined;'):
            self.log.debug(self.driver.execute_script('return window.waScript.waSession != undefined;'))
            t.sleep(5)
        self.log.debug('Getting IDB results...')
        wa_session_list = self.driver.execute_script('return window.waScript.waSession;')
        self.log.debug('Got IDB data...')
        return wa_session_list
        
    def __save_profile__(self, wa_profile_list, filename):
        #Code taken from WaWebSessionHandler-master by jeliebig
        verified_wa_profile_list = False
        for object_store_obj in wa_profile_list:
            if 'key' in object_store_obj:
                if 'WASecretBundle' in object_store_obj['key']:
                    verified_wa_profile_list = True
                    break
        if verified_wa_profile_list:
            self.log.debug('Saving WaSession object to file...')
            with open(filename, 'w') as file:
                json.dump(wa_profile_list, file, indent=4)
                
    def __access_by_obj__(self, wa_profile_list):
        #Code taken from WaWebSessionHandler-master by jeliebig
        verified_wa_profile_list = False
        for object_store_obj in wa_profile_list:
            if 'WASecretBundle' in object_store_obj['key']:
                verified_wa_profile_list = True
                break
        if not verified_wa_profile_list:
            raise ValueError('This is not a valid profile list. Make sure you only pass one session to this method.')
        self.log.debug('Inserting setIDBObjects function...')
        self.driver.execute_script('window.waScript = {};'
                                     'window.waScript.insertDone = 0;'
                                     'window.waScript.jsonObj = undefined;'
                                     'window.waScript.setAllObjects = function (_jsonObj) {'
                                     'window.waScript.jsonObj = _jsonObj;'
                                     'window.waScript.dbName = "wawc";'
                                     'window.waScript.osName = "user";'
                                     'window.waScript.db;'
                                     'window.waScript.transaction;'
                                     'window.waScript.objectStore;'
                                     'window.waScript.clearRequest;'
                                     'window.waScript.addRequest;'
                                     'window.waScript.request = indexedDB.open(window.waScript.dbName);'
                                     'window.waScript.request.onsuccess = function(event) {'
                                     'window.waScript.db = event.target.result;'
                                     'window.waScript.transaction = window.waScript.db.transaction('
                                     'window.waScript.osName, "readwrite");'
                                     'window.waScript.objectStore = window.waScript.transaction.objectStore('
                                     'window.waScript.osName);'
                                     'window.waScript.clearRequest = window.waScript.objectStore.clear();'
                                     'window.waScript.clearRequest.onsuccess = function(clearEvent) {'
                                     'for (var i=0; i<window.waScript.jsonObj.length; i++) {'
                                     'window.waScript.addRequest = window.waScript.objectStore.add('
                                     'window.waScript.jsonObj[i]);'
                                     'window.waScript.addRequest.onsuccess = function(addEvent) {'
                                     'window.waScript.insertDone++;'
                                     '};'
                                     '}'
                                     '};'
                                     '};'
                                     '}')
        self.log.debug('setIDBObjects function inserted.')
        self.log.debug('Writing IDB data...')
        self.driver.execute_script('window.waScript.setAllObjects(arguments[0]);', wa_profile_list)

        self.log.debug('Waiting until all objects are written to IDB...')
        
        while not self.driver.execute_script('return (window.waScript.insertDone == window.waScript.jsonObj.length);'):
            self.log.debug(self.driver.execute_script('return (window.waScript.insertDone == window.waScript.jsonObj.length);'))
            t.sleep(1)
            
        self.log.debug('Reloading WhatsApp Web...')
        self.driver.refresh()
        t.sleep(4)
        
        try:
            self.driver.find_element_by_xpath(self._xpaths_["test"])
            return self.__access_by_obj__(wa_profile_list)
        except Exception as e:
            pass
            
    def __access_by_file__(self, profile_file):
        #Code taken from WaWebSessionHandler-master by jeliebig
        self.log.debug('Reading WaSession from file...')
        with open(profile_file, 'r') as file:
            wa_profile_list = json.load(file)
        self.log.debug('Verifying WaSession object...')
        verified_wa_profile_list = False
        for object_store_obj in wa_profile_list:
            if 'WASecretBundle' in object_store_obj['key']:
                verified_wa_profile_list = True
                break
        if verified_wa_profile_list:
            self.log.debug('WaSession object is valid.')
            self.__access_by_obj__(wa_profile_list)
        else:
            raise ValueError('There might be multiple profiles stored in this file.'
                                 ' Make sure you only pass one WaSession file to this method.')
                                 
    def typer(self,res,textbox):
        try:
            self.log.debug(f'Sending,"{res}"')
            for x in res.split('\n'):
                textbox.send_keys(x)
                textbox.send_keys(Keys.SHIFT+Keys.ENTER)
            textbox.send_keys('\n')
        except Exception as e:
            self.log.warning(e)
        
    def send(self,direct,caption=None):
        try:
            self.log.debug(f'Sending file,"{direct}"')
            attach_btn = self.driver.find_element_by_xpath(self._xpaths_["attachment"])
            attach_btn.click()
            t.sleep(1)
            attach_img_btn = self.driver.find_element_by_xpath(self._xpaths_["attachment_type"])
            attach_img_btn.send_keys(direct)
            t.sleep(3)
            if caption:
                self.typer(caption,self.driver.find_element_by_xpath(self._xpaths_["caption"]))
            send_btn = driver.find_element_by_xpath(self._xpaths_["send_file"])
            send_btn.click()
        except Exception as e:
            self.log.warning(e)
            try:
                self.driver.find_element_by_class_name(self._classes_["close"]).click()
            except:
                pass
            
    def change_log_level(self,log_level):
        if log_level.lower() in self._loglevel_.keys():
            self.log.setLevel(self._loglevel_[log_level.lower()])
        else:
            print("[!]No log level given, fault to warning")
            self.log.setLevel(logging.WARNING)
    def search(self,name):
        try:
            self.log.debug(f"Searching for {name}")
            search = self.driver.find_element_by_xpath(self._xpaths_["search_group"])
            search.send_keys(name + '\n')
            t.sleep(1)
            try:
                search.send_keys(len(name)*Keys.BACKSPACE)
            except:
                pass
        except Exception as e:
            self.log.warning(e)
            try:
                search.send_keys(len(name)*Keys.BACKSPACE)
            except:
                pass
    def chat_textbox(self):
        try:
            return self.driver.find_element_by_xpath(self._xpaths_['textbox'])
        except Exception as e:
            self.log.warning(e)
            return None
        
    def read_lastest_message(self):
        try:
            messages = []
            #print(messages)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            #print(soup.prettify())
            for i in soup.find_all("div", class_="message-in"):
                message = i.find("span", class_="selectable-text")
                if message:
                    #print(message)
                    message2 = message.find("span")
                    if message2:
                        messages.append(message2.text)
            messages = list(filter(None, messages))
            #print(messages[-1])
            return messages[-1]
            #return self.driver.find_elements_by_class_name(self._classes_["message"])[-1].text
        except Exception as e:
            self.log.warning(e)
            return None
            
    def name_of_chat(self):
        try:
            return self.driver.find_element_by_xpath(self._xpaths_["name"]).text
        except:
            self.log.warning(e)
            return None
            
    def admin(self):
        pass
        
    def close(self):
        self.log.warning("Closing...")
        self.driver.quit()
        
        