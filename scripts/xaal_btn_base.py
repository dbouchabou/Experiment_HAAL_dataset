from xaal.lib import Engine, tools, helpers
from xaal.schemas import devices
import platform
import logging

PKG_NAME = 'btn_palpatin'

helpers.setup_console_logger()
logger = logging.getLogger(PKG_NAME)

UUID = tools.get_uuid

BTN0 = UUID('5b71a6bc-d814-11eb-94e4-a4badbf92500')
BTN1 = UUID('9e6448d0-d9b3-11eb-94e4-a4badbf92500')
BTN2 = UUID('c82a3602-d9b3-11eb-94e4-a4badbf92500')
BTN3 = UUID('f7945c38-d9b3-11eb-94e4-a4badbf92500')
BTN4 = UUID('68907b0c-d9b3-11eb-94e4-a4badbf92500')
BTN5 = UUID('33c87ba4-d9b3-11eb-94e4-a4badbf92500')

CLICK_MAP = [
    [BTN1,"Cook Breakf","Cook Lunch"],
    [BTN2,"Cook Dinner","Wash Dishes"],
    [BTN3,"Sleep","Go to Toilets"],
    [BTN4,"Dress","Leave Home"],
    [BTN5,"Watch TV","Read"],
]

DCLICK_MAP = [
    [BTN1,"Eat Breakf","Eat Lunch"],
    [BTN2,"Eat Dinner",None],
    [BTN3,"Sleep in Bed","Bathe"],
    [BTN4,None,"Enter Home"],
    [BTN5,"Take Medicine",None],
]

PC_MENYU_IR = UUID('a2e5b57c-da8c-11eb-88bf-29e1f24a3566')
PC_WINDOWS_KINECT_XSENS = UUID('db206d28-da87-11eb-8902-509a4c5add63')
FISH_EYE = UUID('6d867a2e-da91-11eb-af80-1e00a23e8a62')
TARGETS = [PC_MENYU_IR,PC_WINDOWS_KINECT_XSENS,FISH_EYE]

dev = None

def send(targets,action,body=None):
    engine = dev.engine
    engine.send_request(dev,targets,action,body)


def start_activity(activity):
    logger.info(f"Switch to activity: {activity}")
    tmp = activity.lower()
    tmp = tmp.replace(' ','_')
    send(TARGETS,'start_activity',{'activity':tmp})

#def stop_recording():
#    logger.info(f"Stop recoding")
#    send(TARGETS,'stop_recording')

def search_click_btn(addr):
    for k in CLICK_MAP:
        if k[0]==addr:
            return k[1]
        if (k[0] + 1) == addr:
            return k[2]
    return None

def search_dclick_btn(addr):
    for k in DCLICK_MAP:
        if k[0]==addr:
            return k[1]
        if (k[0] + 1) == addr:
            return k[2]
    return None


def handle_msg(msg):
    if not msg.is_notify():
        return
    # search for the buttons 

    if msg.action == 'click':
        if msg.source == BTN0:
            logger.warning("Start Recording")
            start_activity("Default")

        if msg.source == (BTN0+1):
            logger.warning("Start IR Cams Recording")
            start_activity("Default")

        activity = search_click_btn(msg.source)
        if activity:
            start_activity(activity)
            
    
    if msg.action == 'double_click':
        if msg.source == BTN0:
            logger.warning("Stop Recording All")
            send(TARGETS,'stop_recording')

        if msg.source == (BTN0+1):
            logger.warning("Stop IR Cams Recording")
            send([TARGETS[0],TARGETS[1]],'stop_recording')
        
        activity = search_dclick_btn(msg.source)
        if activity:
            start_activity(activity)

def main():
    global dev

    dev = devices.scenario()
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
