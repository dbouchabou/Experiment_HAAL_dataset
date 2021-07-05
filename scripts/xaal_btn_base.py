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
    [BTN5,"Watch TV","Take Medicine"],
]

DCLICK_MAP = [
    [BTN1,"Eat Breakf","Eat Lunch"],
    [BTN2,"Eat Dinner",None],
    [BTN3,"Sleep in Bed","Bathe"],
    [BTN4,None,"Enter Home"],
    [BTN5,"Read",None],
]

PC_MENYU_IR = UUID('a2e5b57c-da8c-11eb-88bf-29e1f24a3566')
PC_WINDOWS_KINECT_XSENS = UUID('db206d28-da87-11eb-8902-509a4c5add63')
FISH_EYE = UUID('5a72250e-db0a-11eb-a785-1e00a23e8a62')
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
    i = 2
    for k in CLICK_MAP:
        if k[0]==addr:
            return (k[1],i)
        if (k[0] + 1) == addr:
            return (k[2],i+1)
        i = i + 2
    return (None,0)

def search_dclick_btn(addr):
    i = 12
    for k in DCLICK_MAP:
        if k[0]==addr:
            return (k[1],i)
        if (k[0] + 1) == addr:
            return (k[2],i+1)
        i = i +2
    return (None,0)

def set_activity_idx(value):
    if type(value) == int:
        dev.attributes[2].value = value
    else:
        logger.error("setting wrong activity idx")

def dump_activities():
    print("Click MAP:")
    i = 1
    for k in CLICK_MAP:
        print(f"btn:{i} {search_click_btn(k[0])} {search_click_btn(k[0]+1)}")
        i = i + 1
    print()
    print("DClick MAP:")
    i = 1
    for k in DCLICK_MAP:
        print(f"btn:{i} {search_dclick_btn(k[0])} {search_dclick_btn(k[0]+1)}")
        i = i +1 
    print()

def handle_msg(msg):
    if not msg.is_notify():
        return

    if msg.action == 'click':
        if msg.source == BTN0:
            logger.warning("Start Recording")
            start_activity("Default")
            set_activity_idx(1)

        if msg.source == (BTN0+1):
            logger.warning("Start IR Cams Recording")
            #start_activity("Default")
            send([TARGETS[0],TARGETS[1]],'start_activity',{'activity':'default'})
            set_activity_idx(1)

        (activity,idx) = search_click_btn(msg.source)
        if activity:
            start_activity(activity)
            set_activity_idx(idx)
            
    
    if msg.action == 'double_click':
        if msg.source == BTN0:
            logger.warning("Stop Recording All")
            send(TARGETS,'stop_recording')
            set_activity_idx(0)

        if msg.source == (BTN0+1):
            logger.warning("Stop IR Cams Recording")
            send([TARGETS[0],TARGETS[1]],'stop_recording')
            set_activity_idx(0)
        
        (activity,idx) = search_dclick_btn(msg.source)
        if activity:
            start_activity(activity)
            set_activity_idx(idx)

def main():
    global dev
    dump_activities()
    cfg = tools.load_cfg(PKG_NAME)
    if cfg == None:
        cfg = tools.new_cfg(PKG_NAME)
        cfg.write()
    addr = tools.get_uuid(cfg['config']['addr'])
    dev = devices.scenario(addr)
    dev.new_attribute("activity_idx",0)
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
