import cv2
import numpy as np
import os



def test(img1,img2):
    img1=cv2.imread(img1)
    img2=cv2.imread(img2)
    img1=img1.astype(np.int8)
    img2 = img2.astype(np.int8)
    diff=img2-img1
    return diff


if __name__ == '__main__':
    # img1="/home/SENSETIME/wangpengju/github/data/pic_dir/1.jpg"
    # img2="/home/SENSETIME/wangpengju/github/data/pic_dir/2.jpg"
    img_dir="/home/SENSETIME/wangpengju/github/data/pic_dir"
    save_dir="/home/SENSETIME/wangpengju/github/data/data_dir"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    items=os.listdir(img_dir)
    list1=[]
    for i in range(len(items)-1):
        # if i>300:
        #     break
        img1_name="{}.jpg".format(i+1)
        img1_path=os.path.join(img_dir,img1_name)
        img2_name="{}.jpg".format(i+2)
        img2_path=os.path.join(img_dir,img2_name)
        diff_return=test(img1_path,img2_path)
        diff_sum=np.sum(np.maximum(diff_return,-diff_return))
        # print(diff_sum)
        with open("test.txt","a") as f:
            if int(diff_sum)>637441:
                print(i+1,':',diff_sum)
                f.write("frame_{}:".format(i+1))
                f.write("\t")
                f.write("{}\n".format(diff_sum))
            # if np.all(diff_return==0):
            #     f.write("img{}:\n".format(i+1))
            #     f.write(str(diff_return))
            #     f.write("\n")


        # list1.append(diff_return)
        # print("I'm OK!_{}".format(i+1))
        # diff_return=diff_return.astype(np.uint8)
        # save_path=os.path.join(save_dir,img1_name)
        # cv2.imwrite(save_path,diff_return)
    # with open("test.txt","w") as f:
    #     t=len(list1)
    #     for l in list1:
    #         print("I'm {}OK!".format(len(list1)-t))
    #         t=t-1
    #         f.write("frame{}:\n".format(len(list1)-t))
    #         f.write(str(l))





    # print(items)

    # test(img1,img2)