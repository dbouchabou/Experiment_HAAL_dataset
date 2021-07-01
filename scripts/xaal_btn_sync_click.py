from xaal.lib import Engine, tools,helpers
from xaal.schemas import devices
import platform
import pyautogui
import time
import logging
pyautogui.FAILSAFE = False


PKG_NAME = 'btn_darkvador '

helpers.setup_console_logger()

logger = logging.getLogger(PKG_NAME)

BTN0 = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92500')
BTN1 = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92501')

dev = None
sock = None
btn_state = 1

def handle_msg(msg):

    global btn_state

    if not msg.is_notify():
        return
    # search for the buttons 

    if msg.action == 'click':
        if msg.source == BTN0:
            logger.info("Start Recording")
            #get focus Kinect
            #pyautogui.click(180, 15)
            #click on record Kinect
            pyautogui.click(160, 95)
            
            #get focus Xsens
            #pyautogui.click(1425, 15)
            #click on record Xsens
            pyautogui.click(1425, 65)
            
        if msg.source == BTN1:
            logger.info("Stop Recording")
            pyautogui.click(160, 95)
            pyautogui.click(1425, 65)
            

def main():
    global dev

    dev = devices.basic()
    dev.info = '%s@%s' % (PKG_NAME,platform.node())
    engine = Engine()
    engine.add_device(dev)
    engine.add_rx_handler(handle_msg)
    engine.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye bye')
