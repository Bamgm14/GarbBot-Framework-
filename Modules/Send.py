import time as t
import Modules.Blind as b
import Modules.Constant as c
def send(driver,direct,name=None,lst=None,caption=None):
    # open attach menu
    attach_btn = driver.find_element_by_xpath(c.attach_xpath)
    attach_btn.click()
    # Find attach file btn and send screenshot path to input
    t.sleep(1)
    attach_img_btn = driver.find_element_by_xpath(c.attach_type_xpath)
    # TODO - might need to click on transportation mode if url doesn't work
    attach_img_btn.send_keys(direct)
    t.sleep(3)
    if caption!=None:
        send_caption = driver.find_element_by_xpath(c.caption_xpath)
        send_caption.send_keys(caption)
        if name in lst:
            b.blindmode(driver,caption)
    send_btn = driver.find_element_by_xpath(c.send_file_xpath)
    send_btn.click()
