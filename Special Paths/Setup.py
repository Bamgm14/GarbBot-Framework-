import os
import platform
Frame=platform.architecture()[0]
lib=['selenium','bs4','urllib3','matplotlib','numpy','requests']
for x in lib:
    os.system('python3 -m pip install '+str(x)+' --user|| python -m pip install '+str(x)+' --user')
import requests as r
if '64' in Frame:
    WExcutable=r.get('https://eternallybored.org/misc/wget/1.20.3/64/wget.exe')
    a=open('wget.exe','wb')
    a.write(WExcutable.content)
    a.close()
else:
    WExcutable=r.get('https://eternallybored.org/misc/wget/1.20.3/32/wget.exe')
    a=open('wget.exe','wb')
    a.write(WExcutable.content)
    a.close()
os.system('wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_win32.zip')
os.system('setx path "%path%";'+os.getcwd()+'')
