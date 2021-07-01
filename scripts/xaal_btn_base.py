from xaal.lib import Engine, tools, helpers
from xaal.schemas import devices
import platform

PKG_NAME = 'btn_palpatin'

helpers.setup_console_logger()

logger = logging.getLogger(PKG_NAME)

BTN0_LEFT = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92500')
BTN0_RIGHT = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92501')

BTN1_LEFT = tools.get_uuid('9e6448d0-d9b3-11eb-94e4-a4badbf92500')
BTN1_RIGHT = tools.get_uuid('9e6448d0-d9b3-11eb-94e4-a4badbf92500')

BTN2_LEFT = tools.get_uuid('c82a3602-d9b3-11eb-94e4-a4badbf92500')
BTN2_RIGHT = tools.get_uuid('c82a3602-d9b3-11eb-94e4-a4badbf92501')

BTN3_LEFT = tools.get_uuid('f7945c38-d9b3-11eb-94e4-a4badbf92500')
BTN3_RIGHT = tools.get_uuid('f7945c38-d9b3-11eb-94e4-a4badbf92501')

BTN4_LEFT = tools.get_uuid('68907b0c-d9b3-11eb-94e4-a4badbf92500')
BTN4_RIGHT = tools.get_uuid('68907b0c-d9b3-11eb-94e4-a4badbf92501')

BTN5_LEFT = tools.get_uuid('33c87ba4-d9b3-11eb-94e4-a4badbf92500')
BTN5_RIGHT = tools.get_uuid('33c87ba4-d9b3-11eb-94e4-a4badbf92501')


dev = None
sock = None
btn_state = 1

def handle_msg(msg):

    global btn_state

    if not msg.is_notify():
        return
    # search for the buttons 

    if msg.action == 'click':
        if msg.source == BTN0_LEFT:
            logger.info("Start Recording")

        if msg.source == BTN0_RIGHT:
            logger.info("Start IR Cams Recording")
        
        if msg.source == BTN1_LEFT:
            logger.info("Activity Cook Breakf")

        if msg.source == BTN1_RIGHT:
            logger.info("Activity Cook Lunch")

        if msg.source == BTN2_LEFT:
            logger.info("Activity Cook Dinner")

        if msg.source == BTN2_RIGHT:
            logger.info("Activity Wash Dishes")

        if msg.source == BTN3_LEFT:
            logger.info("Activity Sleep")

        if msg.source == BTN3_RIGHT:
            logger.info("Activity Go To Toilets")

        if msg.source == BTN4_LEFT:
            logger.info("Activity Dress")

        if msg.source == BTN4_RIGHT:
            logger.info("Activity Leave Home")

        if msg.source == BTN5_LEFT:
            logger.info("Activity Watch TV")

        if msg.source == BTN5_RIGHT:
            logger.info("Activity Read")
            

    
    if msg.action == 'double_click':
        if msg.source == BTN0_LEFT:
            logger.info("Stop Recording")

        if msg.source == BTN0_RIGHT:
            logger.info("Stop IR Cams Recording")
        
        if msg.source == BTN1_LEFT:
            logger.info("Activity Eat Breakf")

        if msg.source == BTN1_RIGHT:
            logger.info("Activity Eat Lunch")

        if msg.source == BTN2_LEFT:
            logger.info("Activity Eat Dinner")

        if msg.source == BTN2_RIGHT:
            logger.info("NA")

        if msg.source == BTN3_LEFT:
            logger.info("Activity Sleep In Bed")

        if msg.source == BTN3_RIGHT:
            logger.info("Activity Bathe")

        if msg.source == BTN4_LEFT:
            logger.info("NA")

        if msg.source == BTN4_RIGHT:
            logger.info("Activity Enter Home")

        if msg.source == BTN5_LEFT:
            logger.info("Activity Take Medicine")

        if msg.source == BTN5_RIGHT:
            logger.info("NA")
            

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
