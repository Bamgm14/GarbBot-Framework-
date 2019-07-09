from hashlib import md5
import os
def Setup():
    hsh=[]
    for x in os.listdir():
        if os.path.isfile(x) and '.txt' not in x and '.bin' not in x and '.pyc' not in x and '.log' not in x and 'SnL.py' not in x:
            hsh.append(open(x,'rb').read())
        elif '.txt' not in x and '.bin' not in x and '.log' not in x:
            for y in os.listdir(str(os.getcwd())+'\\'+str(x)):
                if os.path.isfile(str(os.getcwd())+'\\'+str(x)+'\\'+y) and '.txt' not in y and '.bin' not in y and '.pyc' not in y and '.log' not in y  and 'SnL.py' not in y:
                    hsh.append(open(str(os.getcwd())+'\\'+str(x)+'\\'+y,'rb').read())
    file=open('Hash.txt','w')
    for x in hsh:
        file.write(md5(x).hexdigest()+'\n')
    file.close()
def Update():
    lib=[]
    for x in os.listdir():
        if os.path.isfile(x) and '.txt' not in x and '.bin' not in x and '.pyc' not in x and '.log' not in x  and 'SnL.py' not in x:
            lib.append(open(x,'rb').read())
        elif '.txt' not in x and '.bin' not in x and '.log' not in x:
            for y in os.listdir(str(os.getcwd())+'\\'+str(x)):
                if os.path.isfile(str(os.getcwd())+'\\'+str(x)+'\\'+y) and '.txt' not in y and '.bin' not in y and '.pyc' not in y and '.log' not in y  and 'SnL.py' not in y:
                    lib.append(open(str(os.getcwd())+'\\'+str(x)+'\\'+y,'rb').read())
    sal=open('Hash.txt','r').read().split('\n')
    for x in range(len(lib)):
        if md5(lib[x]).hexdigest()==sal[x]:
            pass
        else:
            print(x)
            print(md5(lib[x]).hexdigest())
            print('Warning:Module Updated')
            raise RuntimeError('Module Updated')
