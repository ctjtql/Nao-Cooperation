import os 
import time 
import argparse

import numpy as np 
import cv2 
from imutils.video import VideoStream 

from utils import read_img,pre_process
from findShape import find_poly,find_circle
from imgCal import get_momentum 


def main(out_video_path): 
    # init camera 
    print("[INFO] starting video stream...")
    vs = VideoStream(src=1).start()
    time.sleep(2.0)
    
    # use VideoWriter object to save video 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(out_video_path,fourcc, 20.0, (1920,1080))
    
    # begin detect 
    while True: 
        frame = vs.read() 
        
        # get all 6 poly 
        opened = pre_process(frame) 
        poly_6_contours = find_poly(frame,opened,side_num=6) 
        
        # get all circle 
        circle_contours = find_circle(frame,opened)
    
        # draw contours 
        cv2.drawContours(frame,poly_6_contours,-1, (255,0,0), 2)
        cv2.drawContours(frame,circle_contours,-1, (0,255,0), 2)
    
        # find momentum 
        for cnt in poly_6_contours: 
            center_x, center_y = get_momentum(cnt) 
            cv2.circle(frame, (center_x, center_y), 3, 128, -1)  # 绘制中心点
            
        for cnt in circle_contours: 
            center_x, center_y = get_momentum(cnt) 
            cv2.circle(frame,(center_x,center_y),3,128,-1) 
    
        # perspective trans 
        if len(poly_6_contours) >= 4 :  # enough 
            # find 4 max area poly 6  
            # perspective trans 
            # find point 
            pass  
        else:                           # not enough 
            pass 
                
        # imshow 
        cv2.imshow("frame",frame) 
        out.write(frame) 
        
        # break  
        key = cv2.waitKey(1) 
        if key == 27: 
            break 
        
    out.release() 
    cv2.destroyAllWindows()
    vs.stop() 
         
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument("--o",type=str,default="output.avi",
                        help="output file name")
    args = parser.parse_args() 

    # store path 
    if not os.path.exists('video'): 
        os.makedirs('video')
    out_video_path = "./video/" + args.o 

    main(out_video_path)
    

