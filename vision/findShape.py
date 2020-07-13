import cv2
import numpy as np
import argparse 

from utils import read_img,pre_process
from utils import get_blank_img, show_img
from imgCal import get_momentum 

# find proper epsilon 
def find_epsilon(side_num=6): 
    epsilon_dict = {6:0.02,4:0.01}
    try: 
        return epsilon_dict[side_num] 
    except: 
        return 0.01 

def find_poly(img,opened,side_num=6): 
    '''
        Function: get contour of poly with side num 
        Input Params: 
            - img: original image 
            - opened: open image of original image 
            - side_num: side num of poly to be detected, default 6 
        Output Params: 
            - contours: contour of poly 
    '''
    
    # get contours 
    image, contours, hierarchy = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # check contours detected (if need) 
    contour_img = np.zeros(image.shape,np.uint8) 
    contour_img.fill(255) 
    cv2.drawContours(contour_img,contours,-1, (0,0,0), 2)
    show_img(contour_img,'contour img')
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    
    # coutour wash 
    # find max area contour 
    area = [] 
    for cnt in contours: 
        area.append(cv2.contourArea(cnt)) 
    max_index = np.argmax(np.array(area)) 

    print("hierarchy: ",hierarchy.shape) 
    print(hierarchy) 
    
    # begin width search 
    indexs = [max_index] 
    indexs_queue = [max_index]
    while len(indexs_queue) !=0: 
        parent_index = indexs_queue[0] 
        indexs_queue.pop(0)         
        # add child index 
        child_index = hierarchy[0][parent_index][2] 
        
        while child_index != -1: 
            indexs_queue.append(child_index) 
            indexs.append(child_index)
            child_index = hierarchy[0][child_index][0]  
        
    indexs = np.unique(np.array(indexs)) # unique 
    print("indexs: ", indexs) 
    
    wash_contours = [] 
    for i,cnt in enumerate(contours): 
        if i in indexs: 
            wash_contours.append(cnt) 
            
    # check wash contours, if needed 
    wash_contour_img = get_blank_img(image.shape) 
    cv2.drawContours(wash_contour_img,wash_contours,-1,(0,0,0),3) 
    show_img(wash_contour_img,'wash contours') 
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
        
    # approx contours 
    approx_contours = []
    for i,cnt in enumerate(wash_contours):
        epsilon = find_epsilon(side_num)*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        
        # check approx contour if needed 
        # print("approx: ",approx) 
        # temp_img = get_blank_img(image.shape) 
        # cv2.drawContours(temp_img,[approx],-1,(0,0,0),4) 
        # show_img(temp_img,'approx contour')
        # cv2.waitKey(0) 
        
        if side_num==0:  # circle
            if len(approx) < 10:  # core 
                pass
            else:
                approx_contours.append(approx)
        else:            # poly 
            if len(approx) != side_num:  # core 
                pass
            else:
                approx_contours.append(approx)
    
        # check contours detected (if need) 
        # approx_contour_img = np.zeros(image.shape,np.uint8)
        # approx_contour_img.fill(255)
        # cv2.drawContours(approx_contour_img,approx_contours,-1, (0,0,0), 3)
        # cv2.imshow('approx contour img',approx_contour_img)
        # cv2.waitKey(0) 
        # cv2.destroyAllWindows() 
    
    print("find {} side poly: {}".format(side_num,len(approx_contours)))  
    return approx_contours

# find circle 
# Plus: circle's side num is 0 
def find_circle(img,opened): 
    '''
        Function: get contour of circle
        Input Params: 
            - img: original image 
            - opened: open image of original image 
        Output Params: 
            - contours: contour of circles 
        Plus: 
            circle's side num is zero 
    '''
    return find_poly(img,opened,side_num=0)

def main(img_path,side_num): 
    img = read_img(img_path)
    opened = pre_process(img) 
    
    # find poly or circle 
    if side_num == 0:
        approx_contours = find_circle(img,opened)
    else:  
        approx_contours = find_poly(img,opened,side_num=side_num) # temp 
    
    # find momentums
    momentum_img = get_blank_img(img.shape) 
    cv2.drawContours(momentum_img,approx_contours,-1, (0,0,0), 2)
    for contour in approx_contours: 
        center_x,center_y = get_momentum(contour)
        print("x,y: {},{}".format(center_x,center_y))
        cv2.circle(momentum_img, (center_x, center_y), 7, 128, -1)  # 绘制中心点
        
    # show result
    show_img(momentum_img,'momentums')
    cv2.imwrite("./image/momentum.png",momentum_img) 
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument("--pic",type=str,default="try.png",
                        help="picture name")
    parser.add_argument("--folder_path",type=str,default="./image",
                        help="folder path")
    parser.add_argument("--side_num",type=int,default=6,
                        help="side num of poly. if input 10, find circle")
    args = parser.parse_args() 
    
    img_path = args.folder_path + "/" + args.pic 
    side_num = args.side_num 
    
    if __debug__: 
        print("image path: ", img_path) 
     
    main(img_path,side_num)
    


