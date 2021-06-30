import json
import os
from xtcocotools.coco import COCO



def parse(json_path):
    with open(json_path,"r") as f:
        json_dict=json.load(f)
    for i in json_dict:
        print(i)
        #
        print(json_dict[i])




    pass


def show(json_path):
    coco_file=COCO(json_path)
    # print(coco_file.getImgIds("wangchunzi/wangchunzi_1_8.jpg"))
    # coco_file.loadImgs(9848)
    coco_file.getImgIds()

if __name__ == '__main__':
    json_path="/home/SENSETIME/wangpengju/github/data/tracking_data_test/doublehand_nails_test/images/nail_shape_kps_test.json"
    # parse(json_path)
    show(json_path)