import pynput
import time
from pynput.keyboard import Key, Listener
import logging
l=[]
time_list=[]
log_dir = r""
logging.basicConfig(filename = (log_dir + "keyLog.txt"), level=logging.DEBUG, format='%(message)s')


def on_press(key):
   if(str(key)=='Key.backspace' or str(key)=='Key.caps_lock' or str(key)=='Key.shift' or str(key)=='Key.up' or str(key)=='Key.down' or str(key)=='Key.right' or str(key)=='Key.left'): return True
   time_list.append(time.time())
   #logging.info(str(time.time()))
   #logging.info(str(key))
   #print(str(key)+str(time.time())+"\n")
   return False
   
inp=input("Enter the password")

while(True):
    y=input("Do you want to train more?")
    if(y=='n'): break
    
    s=input("Press ENTER to start")
    for i in range(len(inp)):
        with Listener(on_press=on_press) as listener:
            listener.join()
    l.append(tuple(time_list))
    time_list=[]
    print(l)    
