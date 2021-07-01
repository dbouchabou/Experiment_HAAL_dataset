from xaal.lib import Engine, tools, helpers
from xaal.schemas import devices
import platform
import logging

PKG_NAME = 'btn_palpatin'

helpers.setup_console_logger()

logger = logging.getLogger(PKG_NAME)

BTN0_LEFT = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92500')
BTN0_RIGHT = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92501')

BTN1_LEFT = tools.get_uuid('9e6448d0-d9b3-11eb-94e4-a4badbf92500')
BTN1_RIGHT = tools.get_uuid('9e6448d0-d9b3-11eb-94e4-a4badbf92501')

BTN2_LEFT = tools.get_uuid('c82a3602-d9b3-11eb-94e4-a4badbf92500')
BTN2_RIGHT = tools.get_uuid('c82a3602-d9b3-11eb-94e4-a4badbf92501')

BTN3_LEFT = tools.get_uuid('f7945c38-d9b3-11eb-94e4-a4badbf92500')
BTN3_RIGHT = tools.get_uuid('f7945c38-d9b3-11eb-94e4-a4badbf92501')

BTN4_LEFT = tools.get_uuid('68907b0c-d9b3-11eb-94e4-a4badbf92500')
BTN4_RIGHT = tools.get_uuid('68907b0c-d9b3-11eb-94e4-a4badbf92501')

BTN5_LEFT = tools.get_uuid('33c87ba4-d9b3-11eb-94e4-a4badbf92500')
BTN5_RIGHT = tools.get_uuid('33c87ba4-d9b3-11eb-94e4-a4badbf92501')


PC_MENYU = tools.get_uuid('a2e5b57c-da8c-11eb-88bf-29e1f24a3566')
PC_WINDOWS = tools.get_uuid('db206d28-da87-11eb-8902-509a4c5add63')

TARGETS = [PC_WINDOWS,PC_MENYU]

dev = None


def send(targets,action,body=None):
    global dev
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
