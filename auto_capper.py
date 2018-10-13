import datetime
import time
import cap_win as cap

starttime=time.time()
success_saving = 0

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

    time.sleep(5.0 - ((time.time() - starttime) % 5.0))