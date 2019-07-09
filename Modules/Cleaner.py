import shutil,os
clean=['\PictureTemp','\Bike','\Blind']
for x in clean:
    try:
        shutil.rmtree(os.getcwd()+x)
    except:
        pass
    os.mkdir(os.getcwd()+x)
