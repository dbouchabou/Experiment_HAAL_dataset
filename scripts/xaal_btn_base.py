from xaal.lib import Engine, tools, helpers
from xaal.schemas import devices
import platform
import logging

PKG_NAME = 'btn_palpatin'

helpers.setup_console_logger()
logger = logging.getLogger(PKG_NAME)

UUID = tools.get_uuid

BTN0_LEFT = UUID('5b71a6bc-d814-11eb-94e4-a4badbf92500')
BTN0_RIGHT = BTN0_LEFT + 1 

BTN1_LEFT = UUID('9e6448d0-d9b3-11eb-94e4-a4badbf92500')
BTN1_RIGHT = BTN1_LEFT + 1 

BTN2_LEFT = UUID('c82a3602-d9b3-11eb-94e4-a4badbf92500')
BTN2_RIGHT = BTN2_LEFT + 1 

BTN3_LEFT = UUID('f7945c38-d9b3-11eb-94e4-a4badbf92500')
BTN3_RIGHT = BTN3_LEFT + 1 

BTN4_LEFT = UUID('68907b0c-d9b3-11eb-94e4-a4badbf92500')
BTN4_RIGHT = BTN4_LEFT + 1

BTN5_LEFT = UUID('33c87ba4-d9b3-11eb-94e4-a4badbf92500')
BTN5_RIGHT = BTN5_LEFT + 1


PC_MENYU = UUID('a2e5b57c-da8c-11eb-88bf-29e1f24a3566')
PC_WINDOWS = UUID('db206d28-da87-11eb-8902-509a4c5add63')

TARGETS = [PC_WINDOWS,PC_MENYU]

dev = None


def send(targets,action,body=None):
    engine = dev.engine
    engine.send_request(dev,targets,action,body)


def start_activity(activity):
    logger.info(f"Switch to activity: {activity}")
    tmp = activity.lower()
    tmp = tmp.replace(' ','_')
    send(TARGETS,'start_activity',{'activity':tmp})

def stop_activity(activity):
    logger.info(f"Switch to activity: {activity}")
    tmp = activity.lower()
    tmp = tmp.replace(' ','_')
    send(TARGETS,'stop_activity',{'activity':tmp})

def handle_msg(msg):
    if not msg.is_notify():
        return
    # search for the buttons 

    if msg.action == 'click':
        if msg.source == BTN0_LEFT:
            logger.warning("Start Recording")
            start_activity("Default")

        if msg.source == BTN0_RIGHT:
            logger.warning("Start IR Cams Recording")
            start_activity("Default")
        
        if msg.source == BTN1_LEFT:
            start_activity("Cook Breakf")

        if msg.source == BTN1_RIGHT:
            start_activity("Cook Lunch")

        if msg.source == BTN2_LEFT:
            start_activity("Cook Dinner")

        if msg.source == BTN2_RIGHT:
            start_activity("Wash Dishes")

        if msg.source == BTN3_LEFT:
            start_activity("Sleep")

        if msg.source == BTN3_RIGHT:
            start_activity("Go To Toilets")

        if msg.source == BTN4_LEFT:
            start_activity("Dress")

        if msg.source == BTN4_RIGHT:
            start_activity("Leave Home")

        if msg.source == BTN5_LEFT:
            start_activity("Watch TV")

        if msg.source == BTN5_RIGHT:
            start_activity("Read")
    
    if msg.action == 'double_click':
        if msg.source == BTN0_LEFT:
            #start_activity("Stop Recording")
            logger.warning("Start Recording")
            stop_activity("Default")

        if msg.source == BTN0_RIGHT:
            #start_activity("Stop IR Cams Recording")
            logger.warning("Start IR Cams Recording")
            stop_activity("Default")
        
        if msg.source == BTN1_LEFT:
            start_activity("Eat Breakf")

        if msg.source == BTN1_RIGHT:
            start_activity("Eat Lunch")

        if msg.source == BTN2_LEFT:
            start_activity("Eat Dinner")

        if msg.source == BTN2_RIGHT:
            start_activity("NA")

        if msg.source == BTN3_LEFT:
            start_activity("Sleep In Bed")

        if msg.source == BTN3_RIGHT:
            start_activity("Bathe")

        if msg.source == BTN4_LEFT:
            start_activity("NA")

        if msg.source == BTN4_RIGHT:
            start_activity("Enter Home")

        if msg.source == BTN5_LEFT:
            start_activity("Take Medicine")

        if msg.source == BTN5_RIGHT:
            start_activity("NA")
            

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
