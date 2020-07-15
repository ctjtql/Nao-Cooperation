import os 
import time
import almath
import argparse
import xml.dom.minidom

import numpy as np
from naoqi import ALProxy

xml_folder_path = "./xml"

# go to user defined posture 
def go_to_posture(motionProxy,posture_name): 
    '''
        Function: go to Posture (user defined)
    '''
    file_path = xml_folder_path +'/' + posture_name + ".xml" 
    
    # Opening the file 
    names = [] 
    angles = [] 

    try: 
        dom = xml.dom.minidom.parse(file_path)
    except: 
        print "Cannot Open the file"
        return 
    
    # parse file 
    root = dom.documentElement
    motors = root.getElementsByTagName('Motor') 
    for motor in motors: 
        name = str(motor.getElementsByTagName('name')[0].firstChild.data)
        angle = float(motor.getElementsByTagName('value')[0].firstChild.data)
        names.append(name) 
        angles.append(angle) 
        
    # change posture 
    times = 1.0
    isAbsolute = True 
    motionProxy.wakeUp() 
    motionProxy.angleInterpolation(names, angles, times, isAbsolute)

# get current user-defined posture list 
def get_current_posture(): 
    '''
        Fucntion: get current posture list [user defined]
        Ouput Params: 
            - posture_list: list of posture name 
    '''
    file_list = os.listdir(xml_folder_path) 
    posture_list = [file_name[:-4] for file_name in file_list]
    return posture_list
     

def main(robotIP, PORT, file_name):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    
    go_to_posture(motionProxy,file_name)

    time.sleep(3.0) 
    
     
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("--n",type=str,default="try",
                        help="posture name")
    args = parser.parse_args()
    
    main(args.ip, args.port,args.n)