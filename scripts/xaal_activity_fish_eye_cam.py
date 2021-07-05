from xaal.lib import Device, Engine, tools,helpers
from xaal.schemas import devices
import logging
import subprocess
import os
import time


PKG='activity_switcher_fish_eye_cam'

helpers.setup_console_logger()
logger = logging.getLogger(PKG)


dev = None

#base_directory = "/run/user/1000/gvfs/smb-share:server=10.77.3.109,share=e/dataset/tmp"
#base_directory = "/Volumes/desktop-hi76jc1/dataset/subject_tmp"
base_directory = "E:\dataset\subject_tmp"


def start_activity(_activity):

    global processus_ir_cam_big

    if dev.attributes[0].value != True:
        logger.debug(f"Wainting for 10s Fish Eye")
        time.sleep(10)

        dev.attributes[0].value = True
        dev.attributes[1].value = _activity

        logger.debug(f"Starting recording Fish Eye")

        path_big = base_directory+"/"

        if not os.path.exists(path_big):
            os.makedirs(path_big)

        processus_ir_cam_big = subprocess.Popen(args=["ffmpeg",
                                                        "-i",
                                                        "rtsp://admin:AWITIR@10.77.3.110:554", 
                                                        "-f", 
                                                        "segment",
                                                        "-segment_time",
                                                        "1800",
                                                        path_big+"salon_capture-%03d.mp4"
                                                        ], stdout=subprocess.PIPE)
    

def stop_recording():
    logger.debug(f"Stop recording")
    dev.attributes[0].value = False
    dev.attributes[1].value = None

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
    dev.info = 'FISH EYE CAM'

    eng = Engine()
    eng.add_device(dev)
    eng.run()


if __name__ ==  '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye ..")



    
