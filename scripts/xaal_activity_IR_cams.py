from xaal.lib import Device, Engine, tools,helpers
from xaal.schemas import devices
import logging
import subprocess
import os
import time


PKG='activity_switcher_kinect_xsens'

helpers.setup_console_logger()
logger = logging.getLogger(PKG)


dev = None

base_directory = "/run/user/1000/gvfs/smb-share:server=10.77.3.109,share=e/dataset/subject_tmp"


def start_activity(_activity):

    global processus_ir_cam_big
    global processus_ir_cam_small

    if dev.attributes[0].value == True:
        stop_recording_optrix()
	time.sleep(1)


    if dev.attributes[0].value != True:
        path_small = base_directory+"/"+_activity+"/mini_IR"
        filename = "/miniIR.mp4"
    
        if not os.path.exists(path_small):
            os.makedirs(path_small)
        processus_ir_cam_small = subprocess.Popen(args=["ffmpeg","-i","rtsp://xaal-c.enstb.org:8554/flir1", path_small+filename], stdout=subprocess.PIPE)
	
        time.sleep(10)


    dev.attributes[0].value = True
    dev.attributes[1].value = _activity
    logger.debug(f"Starting recording {_activity}")

    path_big = base_directory+"/"+_activity+"/Optrix"

    if not os.path.exists(path_big):
        os.makedirs(path_big)

    processus_ir_cam_big = subprocess.Popen(args=["rosrun","optris_drivers","camera.py", "-a", _activity, "-d",path_big], stdout=subprocess.PIPE)
    
    

def stop_recording():
    logger.debug(f"Stop recording")
    dev.attributes[0].value = False
    dev.attributes[1].value = None

    global processus_ir_cam_big
    global processus_ir_cam_small

    processus_ir_cam_big.terminate()
    processus_ir_cam_small.terminate()


def stop_recording_optrix():
    logger.debug(f"Stop recording Optrix")

    global processus_ir_cam_big

    processus_ir_cam_big.terminate()


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
    dev.info = 'IR CAMS'

    eng = Engine()
    eng.add_device(dev)
    eng.run()


if __name__ ==  '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye ..")



    
