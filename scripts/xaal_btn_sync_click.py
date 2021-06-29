from xaal.lib import Engine, tools
from xaal.schemas import devices
import platform
import socket

PKG_NAME = 'btn_relay'

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
        if msg.source in [BTN1]:
            #print("BNT 1")
            if btn_state == 1:
                print("Start Recording")
                btn_state = 2
            else:
                print("Stop Recording")
                btn_state = 1
            

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
