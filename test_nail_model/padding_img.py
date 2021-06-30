import cv2
import matplotlib.pyplot as plt
import os

# img = cv2.imread('C:\\Elag\\data\\kaggle\\landmark-recognition-challenge\\data\\test\\00b8b0b4a977c786.jpg')

# # 填充固定像素值
# img1 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_CONSTANT,value=[255,255,255])
# img2 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_DEFAULT)
# img3 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_ISOLATED)
# # 靠近边界的50个像素翻折出去（轴对称）
# img4 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REFLECT)
# img5 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REFLECT101)
# img6 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REFLECT_101)
# # 根据对边50像素填充
# img7 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_WRAP)
# # 根据图像的边界的像素值，向外扩充图片，每个方向扩充50个像素。
# img8  = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REPLICATE)

# cv2.imshow('BORDER_CONSTANT', img1)
# cv2.imshow('BORDER_DEFAULT', img2)
# cv2.imshow('BORDER_ISOLATED', img3)
# cv2.imshow('BORDER_REFLECT', img4)
# cv2.imshow('BORDER_REFLECT101', img5)
# cv2.imshow('BORDER_REFLECT_101', img6)
# cv2.imshow('BORDER_WRAP', img7)
# cv2.imshow('BORDER_REPLICATE', img8)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

if __name__ == '__main__':
    img_root="/home/SENSETIME/wangpengju/github/data/tracking_data/test/ori"
    tar_root="/home/SENSETIME/wangpengju/github/data/tracking_data/test/tar"
    if not os.path.exists(tar_root):
        os.makedirs(tar_root)
    for root,dirs,files in os.walk(img_root):
        for file in files:
            print(file)
            ori_path=os.path.join(root,file)
            tar_path=os.path.join(tar_root,file)
            print(tar_path)
            img=cv2.imread(ori_path)
            print(img.shape)
            padding_num=300
            img=cv2.copyMakeBorder(img,padding_num,padding_num,padding_num,padding_num,cv2.BORDER_CONSTANT,value=[0,0,0])
            cv2.imwrite(tar_path,img)
