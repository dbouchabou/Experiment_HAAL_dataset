from xaal.lib import Device, Engine, tools,helpers
from xaal.schemas import devices
import logging
import pyautogui


pyautogui.FAILSAFE = False

PKG='activity_switcher_kinect_xsens'

helpers.setup_console_logger()
logger = logging.getLogger(PKG)


dev = None


def start_activity(_activity):
    if dev.attributes[0].value == False and dev.attributes[1].value != _activity:

        dev.attributes[0].value = True
        dev.attributes[1].value = _activity
        logger.debug(f"Starting recording {_activity}")

        # click on record Kinect
        pyautogui.click(160, 95)

        # click on record Xsens
        pyautogui.click(1425, 65)

def stop_recording():
    logger.debug(f"Stop recording")
    dev.attributes[0].value = False
    dev.attributes[1].value = None

    # Stop Kinect
    pyautogui.click(160, 95)

    # Stop xsens
    pyautogui.click(1425, 65)

    # Click on "RECORD" to prepare the next record
    pyautogui.click(180, 45)

def main():
    global dev
    cfg = tools.load_cfg(PKG)
    if cfg == None:
        cfg = tools.new_cfg(PKG)
        cfg.write()
    addr = tools.get_uuid(cfg['config']['addr'])

    dev = devices.hmi(addr)
    dev.add_method('start_activity',start_activity)
    dev.add_method('stop_recording',stop_recording)
    dev.new_attribute("state",None)
    dev.new_attribute("activity",None)
    dev.info = 'KINECT CAMS'
    
    eng = Engine()
    eng.add_device(dev)
    eng.run()


if __name__ ==  '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye ..")



    
