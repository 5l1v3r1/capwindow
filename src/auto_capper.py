import configparser
import datetime
import time

def get_settings():
    config = configparser.ConfigParser()
    config.read('capwin.ini')
    ss_interval = config['Screenshot']['ss_interval']
    return int(ss_interval)

starttime=time.time()
success_saving = 0
ss_interval = float(get_settings() / 1000)

import cap_win as cap

while True:

    now = datetime.datetime.now()
    loop_date = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        cap.save_screenshot()
        success_saving = 1
    except:
        success_saving = 0
    
    if success_saving:
        print(loop_date + " :: Screenshot saved.")
    
    else:
        print(loop_date + " :: Error while saving screenshot...")

    time.sleep(ss_interval - ((time.time() - starttime) % ss_interval))