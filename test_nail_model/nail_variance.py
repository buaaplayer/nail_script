import os
import json
import sys

# def _parse_txt(txt_path):
#     with open(txt_path,'r') as f:
#         items=f.readlines()
#     return items
import numpy as np


def json_formt(data_list):
    """convert pred_data into json form.
    json_contains:
        -image_name
        -image_path?
        -detection_pred
        -kps_pred
    """
    images={}
    images_list=[]
    img = {}
    nail_dic={}
    nail_list=[]
    for i in range(len(data_list)):
        if str(data_list[i]).strip().endswith('jpg') or str(data_list[i]).strip().endswith('png') or len(str(data_list[i]).split("/"))>1:
            if len(nail_list)>0:
                # print(nail_list)
                img["pre"] = nail_list
                images_list.append(img)
                # print(images_list[-1])
                nail_list=[]
                # print(img)
                img = {}
            img["img_name"] = str(data_list[i]).strip()


        else:
            temp_list=str(data_list[i]).strip().split(",")
            if len(temp_list)==2:
                rec=str(temp_list[0]).strip().replace("\n","")
                kps=str(temp_list[1]).strip().replace("\n","")
                nail_dic["rec"]=rec
                nail_dic["kps"]=kps
                # print(nail_dic)
                # print(id(nail_dic))
                nail_list.append(nail_dic)
                nail_dic={}
                # print(nail_list)
            else:
                print("length not 2")
            temp_list=[]
            # print('0:', images_list[0])
            # print('-1:', images_list[-1])
    images["images"]=images_list
    print(images_list)
    return json.dumps(images,sort_keys=True,indent=4,separators=(",",":"),ensure_ascii=False)

def parse_pred_txt(path_txt):
    "parse the pred txt and find all image_names who have pred_result,the return the pred_list and pred_result"
    # list_for_save=[]
    index_start=0
    #name_list=[]
    nail_datas=[]
    with open(path_txt,"r") as f:
        items=f.readlines()
    for i in range(len(items)):
        cout=0
        if items[i].startswith("start--"):
            index_start=i
            temp_list = []
            continue
        elif items[i].startswith("end--"):
            cout+=1
            if cout==4:
                break
            index_end=i
            temp_list=items[index_start+1:index_end]
            nail_datas.append(temp_list)
    print('nail_datas==>',len(nail_datas))
    return nail_datas



def compute_nail_variance():
    pass

def _xywh_to_xyxy(xywh_list):
    return [float(xywh_list[0]),float(xywh_list[1]),float(xywh_list[0])+float(xywh_list[2]),float(xywh_list[1])+float(xywh_list[3])]

def _convert_recs_format(rec_list):
    """转换recs格式"""
    new_rec_list=[]
    for item in rec_list:
        xyxy=[float(sub_item) for sub_item in item.split(" ")]
        new_rec_list.append(xyxy)
    return new_rec_list

def _compute_iou(rec1, rec2):
    """
    computing IoU
    :param rec1: (x0, y0, x1, y1), which reflects
            (left, top, right, bottom)
    :param rec2: (x0, y0, x1, y1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[0], rec2[0])
    right_line = min(rec1[2], rec2[2])
    top_line = max(rec1[1], rec2[1])
    bottom_line = min(rec1[3], rec2[3])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / (sum_area - intersect)) * 1.0


def main(txt_path):
    nail_datas=parse_pred_txt(txt_path)
    pseudo_gt_recs=[]
    for item in nail_datas:
        if len(item)==5:
            # nonlocal pseudo_gt
            pseudo_gt_recs=[sub_item.strip().replace("\n","").split(",")[0] for sub_item in item]
            break
    format_pseudo_gt_recs=_convert_recs_format(pseudo_gt_recs)
    all_pre_recs_kps=[]
    nail_list_0 = []
    nail_list_1 = []
    nail_list_2 = []
    nail_list_3 = []
    nail_list_4 = []
    for i in range(len(nail_datas)):
        pre_recs_kps_single_img=[sub_item.strip().replace("\n","").split(",") for sub_item in nail_datas[i]]
        all_pre_recs_kps.append(pre_recs_kps_single_img)
        for item in pre_recs_kps_single_img:
            # format_item_rec=_xywh_to_xyxy(item[0].split(" "))
            format_item_rec = [float(sub_it) for sub_it in item[0].split(" ")]
            single_img_nail_ious = []
            for i in range(len(format_pseudo_gt_recs)):
                single_nail_iou=_compute_iou(format_item_rec,format_pseudo_gt_recs[i])
                single_img_nail_ious.append(single_nail_iou)
            max_iou=max(single_img_nail_ious)
            # if max_iou<0.8:
            #     print("max_iou==>",max(single_img_nail_ious))
            max_index=single_img_nail_ious.index(max_iou)
            if max_index == 0:
                nail_list_0.append([float(sub_i)for sub_i in item[1].split(" ")])
            elif max_index == 1:
                nail_list_1.append([float(sub_i)for sub_i in item[1].split(" ")])
            elif max_index == 2:
                nail_list_2.append([float(sub_i)for sub_i in item[1].split(" ")])
            elif max_index ==3:
                nail_list_3.append([float(sub_i)for sub_i in item[1].split(" ")])
            elif max_index == 4:
                nail_list_4.append([float(sub_i)for sub_i in item[1].split(" ")])
            else:
                print("index_error!")
    array0 = np.array(nail_list_0)
    array1 = np.array(nail_list_1)
    array2 = np.array(nail_list_2)
    array3 = np.array(nail_list_3)
    array4 = np.array(nail_list_4)
    # print('array0==>',array0[0][1])
    # print(array0)
    # np_std0 = np.std(array0, axis=1)
    # print(np_std0)
    np_std0=np.mean(np.std(array0,axis=0))
    np_std1 = np.mean(np.std(array1, axis=0))
    np_std2 = np.mean(np.std(array2, axis=0))
    np_std3 = np.mean(np.std(array3, axis=0))
    np_std4 = np.mean(np.std(array4, axis=0))
    print("np_std0==>", np_std0)
    print("np_std1==>", np_std1)
    print("np_std2==>", np_std2)
    print("np_std3==>", np_std3)
    print("np_std4==>", np_std4)
    print("all_avg_std:",(np_std0+np_std1+np_std2+np_std3+np_std4)/5.0)

if __name__ == '__main__':
    """
    argv[1]:txt_dir
    argv[2]:model_name
    argv[3]:mode
    argv[4]:smooth_factor
    """
    # txt_path="/home/SENSETIME/wangpengju/github/data/tracking_data_test/video_result_{}_{}_smooth{}.txt".format(sys.argv[1],sys.argv[2],sys.argv[3])
    txt_path = "{}/video_result_{}_{}_smooth{}.txt".format(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4])
    main(txt_path)








