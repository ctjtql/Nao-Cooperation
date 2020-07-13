import numpy as np
import cv2
import argparse


# get blank img 
def get_blank_img(shape):
    blank_img = np.zeros(shape,np.uint8)
    blank_img.fill(255)
    return blank_img

# show img (in limited size)
def show_img(img,img_name="show",size_limit=512): 
    print("original size", img.shape) 
    if img.shape[0] > size_limit: 
        h_new = size_limit 
        w_new = int(img.shape[1] * h_new / img.shape[0])  
        img = cv2.resize(img,(w_new,h_new)) 
    if img.shape[1] > size_limit: 
        w_new = size_limit 
        h_new = int(img.shape[0] * w_new / img.shape[1]) 
        img = cv2.resize(img,(w_new,h_new)) 

    print("new shape",img.shape) 
    cv2.imshow(img_name, img)
    
    return True 

# 读取图片
def read_img(imgPath,mode=1):
    img = cv2.imread(imgPath, mode)
    if __debug__: 
        show_img(img,'src')
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 
    return img

# 高斯滤波
def GausBlur(src):
    dst = cv2.GaussianBlur(src, (5, 5), 1.5)
    if __debug__: 
        show_img(dst,'Gaus Blur')
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
    return dst

# 灰度处理
def Gray_img(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    if __debug__: 
        show_img(gray,'gray') 
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
    return gray

# 二值化
def threshold_img(src):
    ret, binary = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    if __debug__: 
        print("binary thre: ", ret)
        show_img(binary,'threshold') 
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
    return binary

# 开运算操作
def open_mor(src):
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel, iterations=3)  # iterations进行3次操作
    if __debug__: 
        show_img(opening,'open') 
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
    return opening

# Pre-process
def pre_process(img): 
    # img = GausBlur(img)
    img = Gray_img(img)
    img = threshold_img(img)
    # img = open_mor(img)
    
    return img 

# inverse img 
def inverse_img(image):
    ''' 
        Function: inv img 
        Input Param: 
            - image: original image 
        Output Param: 
            - image: image after inverse 
    ''' 
    # get original h & w 
    height, width= image.shape
    for row in range(height):
        for wid in range(width):
            pv = image[row, wid]
            image[row, wid] = 255 - pv
    
    # cv2.imshow("AfterDeal", image)
    # cv2.waitKey(0)
    
    return image

# img outline 
def Img_Outline(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,gray_img = ret, im2 = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)                     # 高斯模糊去噪（设定卷积核大小影响效果）
    blurred = inverse_img(blurred)
    _, RedThresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)  # 设定阈值165（阈值影响开闭运算效果）
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))          # 定义矩形结构元素
    closed = cv2.morphologyEx(RedThresh, cv2.MORPH_CLOSE, kernel)       # 闭运算（链接块）
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)           # 开运算（去噪点）
    return img, gray_img, RedThresh, closed, opened

if __name__=="__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument("--pic",type=str,default="try.png",
                        help="picture name")
    parser.add_argument("--folder_path",type=str,default="./",
                        help="folder path")
    args = parser.parse_args() 

    img_path = args.folder_path + "/" + args.pic 
    if __debug__: 
        print("image path: ", img_path) 
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
