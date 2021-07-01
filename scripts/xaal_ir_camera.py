from xaal.lib import Engine, tools,helpers
from xaal.schemas import devices
import platform
#import pyautogui
import time
import logging
import subprocess
#pyautogui.FAILSAFE = False
import argparse
import json


PKG_NAME = 'btn_darkvador '

helpers.setup_console_logger()

logger = logging.getLogger(PKG_NAME)

BTN0 = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92500')
BTN1 = tools.get_uuid('5b71a6bc-d814-11eb-94e4-a4badbf92501')

activity_name = "sit"
dest_folder = "/run/user/1000/gvfs/smb-share:server=10.77.3.109,share=e/dataset/test"


dev = None
sock = None
btn_state = 1

def handle_msg(msg, action, directory):

	global a_child_process

	if not msg.is_notify():
		return
		# search for the buttons 

	if msg.action == 'click':
		if msg.source == BTN0:
			logger.info("Start Recording")
			
			d2 = "/media/student/TOSHIBA EXT/test"
			d3 ="/home/student/catkin_ws/Image_Data/test"
			d4 = "/run/user/1000/gvfs/smb-share:server=10.77.3.109,share=e/dataset/test"
			a_child_process = subprocess.Popen(args=["rosrun","optris_drivers","camera.py", "-a", action, "-d",directory], stdout=subprocess.PIPE)
		    
		if msg.source == BTN1:
			logger.info("Stop Recording")
			a_child_process.terminate()
	    
def load_config(config_path):
	f = open(config_path)

	return json.load(f)


def main():
    global dev

    dev = devices.basic()
    dev.info = '%s@%s' % (PKG_NAME,platform.node())
    engine = Engine()
    engine.add_device(dev)
    engine.add_rx_handler(handle_msg,act)
    engine.run()

if __name__ == '__main__':
	p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='')
	p.add_argument('--c', dest='config_file', action='store', default='', help='config file', required=True)

	args = p.parse_args()

	config_file = str(args.config_file)

	try:
		main()
	except KeyboardInterrupt:
		print('Bye bye')

