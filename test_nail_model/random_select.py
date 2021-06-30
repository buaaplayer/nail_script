import os
import random
from shutil import copyfile




def get_file_names(img_root):
    file_path_list = []
    for root,dirs,files in os.walk(img_root):
        # print(root)
        for file in files:
            file_path=os.path.join(root,file)
            file_path_list.append(file_path)
    # sub_file_path_list=random.sample(file_path_list,int(len(file_path_list)/3))
    sub_file_path_list = random.sample(file_path_list, 12000)
    return sub_file_path_list

def main(img_root,new_img_root):
    sub_file_path_list=get_file_names(img_root)
    for item in sub_file_path_list:
        print(len(sub_file_path_list))
        sub_dir=item.split("/")[-3:]
        str_sub_path="/".join(sub_dir)
        new_path=os.path.join(new_img_root,str_sub_path)
        new_dir=os.path.dirname(new_path)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        copyfile(item,new_path)





if __name__ == '__main__':
    img_root='/home/SENSETIME/wangpengju/Downloads/video/20210507_all_frames'
    new_img_root='/home/SENSETIME/wangpengju/Downloads/video/20210507_12000_frames'
    if not os.path.exists(new_img_root):
        os.makedirs(new_img_root)
    main(img_root,new_img_root)
