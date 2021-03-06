from xaal.lib import Device, Engine, tools,helpers
from xaal.schemas import devices
import logging

PKG='activity_switcher_sample'

helpers.setup_console_logger()
logger = logging.getLogger(PKG)


dev = None


def start_activity(_activity):
    dev.attributes[0].value = True
    dev.attributes[1].value = _activity
    logger.debug(f"Starting {_activity}")

def stop_activity():
    logger.debug(f"Stop activity")
    dev.attributes[0].value = False
    dev.attributes[1].value = None

def main():
    global dev
    cfg = tools.load_cfg(PKG)
    if cfg == None:
        cfg = tools.new_cfg(PKG)
        cfg.write()
    addr = tools.get_uuid(cfg['config']['addr'])

    dev = devices.scenario(addr)
    dev.add_method('start_activity',start_activity)
    dev.add_method('stop_activity',stop_activity)
    dev.new_attribute("state",None)
    dev.new_attribute("activity",None)
    
    eng = Engine()
    eng.add_device(dev)
    eng.run()


if __name__ ==  '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye ..")



    
