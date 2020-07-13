import numpy as np 
import cv2 
import argparse

def main(img_path,color='r'): 
    pass 


if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument("--pic",type=str,default="temp.png",
                        help="picture name")
    parser.add_argument("--folder_path",type=str,default="./image",
                        help="folder path")
    parser.add_argument("--color",type=str,default='b',
                        help="color type 'r/g/b'")
    args = parser.parse_args() 
    
    img_path = args.folder_path + "/" + args.pic 
    color = args.color 
    
    if __debug__: 
        print("image path: ", img_path) 
     
    main(img_path,color)