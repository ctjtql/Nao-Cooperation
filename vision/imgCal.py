import numpy as np 
import cv2 

# get momentum 
def get_momentum(contour): 
    ''' 
        Function: get momentum 
        Input param: 
            - contour 
        Output param: 
            - center_x, center_y: position of momentum 
    ''' 
    
    M = cv2.moments(contour)  
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])
    return center_x,center_y

# perspective trans 
def Perspective_transform(box,original_img):
    '''
        Function: Perspective Transform
        Input Params: 
            - box: perspective points 
            - original_img: img to change 
        Output Params: 
            - result_img: img after transform 
    '''
    
    # get original shape 
    H_rows, W_cols= original_img.shape[:2]

    # cal trans matrix 
    pts1 = np.float32([box[0], box[1], box[2], box[3]])
    pts2 = np.float32([[0, 0],[800,0],[0, 800],[800,800],])

    # 生成透视变换矩阵；进行透视变换
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result_img = cv2.warpPerspective(original_img, M, (800,800))

    return result_img