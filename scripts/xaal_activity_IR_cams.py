from xaal.lib import Device, Engine, tools,helpers
from xaal.schemas import devices
import logging
import subprocess


PKG='activity_switcher_kinect_xsens'

helpers.setup_console_logger()
logger = logging.getLogger(PKG)


dev = None

directory = "/run/user/1000/gvfs/smb-share:server=10.77.3.109,share=e/dataset/test"


def start_activity(_activity):
    dev.attributes[0].value = True
    dev.attributes[1].value = _activity
    logger.debug(f"Starting {_activity}")

    global processus_ir_cam_big
    global processus_ir_cam_small

    processus_ir_cam_big = subprocess.Popen(args=["rosrun","optris_drivers","camera.py", "-a", dev.attributes[1].value, "-d",directory], stdout=subprocess.PIPE)
    

    path_small = directory+"/"+_activity+"filename210701.mp4"
    processus_ir_cam_small = subprocess.Popen(args=["ffmpeg","-i","rtsp://xaal-c.enstb.org:8554/flir1", path_small], stdout=subprocess.PIPE)
    

def stop_activity():
    logger.debug(f"Stop activity")
    dev.attributes[0].value = False
    dev.attributes[1].value = None

    global processus_ir_cam_big
    global processus_ir_cam_small

    processus_ir_cam_big.terminate()
    processus_ir_cam_small.terminate()

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
    dev.new_attribute("processus_ir_cam_big",None)
    dev.new_attribute("processus_ir_cam_small",None)
    
    eng = Engine()
    eng.add_device(dev)
    eng.run()


if __name__ ==  '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye ..")



    
