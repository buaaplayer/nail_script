import json
import os
from shutil import copyfile,copy


import json
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except(ValueError):
        print("not json data")
        return False
    return True


def parse_json_data(json_path):
    with open(json_path,"r") as f:
        json_dict=json.loads(f)
    # print(json_dict)
    return json_dict
def parse_json_file(json_path):
    with open(json_path,"r") as f:
        json_dict=json.load(f)
    return json_dict


def find_test_img(img_root,tar_root,json_path):
    temp_path_list=[]
    temp_name_list=[]
    tar_path_list=[]
    json_dict_return=parse_json_file(json_path)
    for item in json_dict_return["images"]:
        file_name=item["file_name"]
        file_path=os.path.join(img_root,file_name)
        if os.path.isfile(file_path):
            temp_path_list.append(file_path)
            temp_name_list.append(file_name)
            tar_path = os.path.join(tar_root, file_name)
            tar_dir=os.path.join(tar_root,'/'.join(file_name.split('/')[:-1]))
            print(tar_dir)
            if not os.path.exists(tar_dir):
                os.makedirs(tar_dir)
            tar_path_list.append(tar_dir)
            copyfile(file_path,tar_path)
        else:
            continue
    raw_path_name="raw_path_test.txt"
    raw_name = "name_test.txt"
    tar_path_name="tar_path_test.txt"
    raw_path_name_path=os.path.join(tar_root,raw_path_name)
    raw_name_path=os.path.join(tar_root,raw_name)
    tar_path_name_path=os.path.join(tar_root,tar_path_name)
    raw_path_f=open(raw_path_name_path,"w")
    raw_name_f=open(raw_name_path,"w")
    tar_path_f=open(tar_path_name_path,"w")
    for i in range(len(tar_path_list)):
        raw_path_f.write(temp_path_list[i]+"\n")
        raw_name_f.write(temp_name_list[i]+"\n")
        tar_path_f.write(tar_path_list[i]+"\n")
    raw_path_f.close()
    raw_name_f.close()
    tar_path_f.close()




if __name__ == '__main__':
    json_path="/home/SENSETIME/wangpengju/github/data/tracking_data/ori_image/nails_data_images/images/nail_shape_kps_test_v2.json"
    img_root="/home/SENSETIME/wangpengju/github/data/tracking_data/ori_image/nails_data_images/images"
    tar_root="/home/SENSETIME/wangpengju/github/data/tracking_data/ori_image/nails_data_images/test"
    if not os.path.exists(tar_root):
        os.makedirs(tar_root)
    # parse_json_file(json_path)
    find_test_img(img_root,tar_root,json_path)
    print("well done!")