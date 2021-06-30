import os
from shutil import copyfile
import datetime
import time

import cv2
import numpy as np
import math
import json
import sys
import time


np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

# def test_method(path_txt):
#     "test some method"
#     with open(path_txt,"r") as f:
#         list_f=f.readlines()
#         for item in list_f:
#             # print(item)

iou_loss=0


def test():
    list1=[6.791491244539805, 6.40923416540493, 6.640163294910318, 6.443945850842066, 6.503887789120083, 6.5391887161309965, 6.416465766537667, 6.692980766887194, 6.4021632665195884, 6.863057312045999, 6.5030842778831115, 6.999332817836235, 6.629824783661295, 7.108824615727446, 6.789616384986874, 7.180015711323052, 6.9531041380025185, 7.2015498124738695, 7.060667508925, 7.174498267495854, 7.130465851709857, 7.064095823536076, 7.148035964091618, 6.909821666037696, 7.1419292786906405, 6.730263688282637, 7.1183060483237, 6.60084481171455, 7.055257199929398, 6.522100710491419, 6.948711609907079, 6.451177451974802]
    list2=[6.904133826670603, 7.20891774899566, 7.084109694046109, 7.178578799208369, 7.241782680892742, 7.089527105007595, 7.313510470393138, 6.92430365307147, 7.286441195155514, 6.74549739800484, 7.214185968161763, 6.612936623920345, 7.108143629375079, 6.504267498543187, 6.98278006367362, 6.419271016155962, 6.833798311238009, 6.396617426747842, 6.62059741945438, 6.447070193318144, 6.468669471559625, 6.610018479411315, 6.382349964214421, 6.813804683084502, 6.396303738035628, 7.030936513329811, 6.497444334281739, 7.11116796497286, 6.6314054213779805, 7.151792370539717, 6.7660060228743, 7.190198978689087]
    test_num=compute_std(list1,list2)
    print("test_num",test_num)

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
    # print(images_list)
    return json.dumps(images,sort_keys=True,indent=4,separators=(",",":"),ensure_ascii=False)

def _parse_json(json_path):
    with open(json_path,"r") as f:
        return json.load(f)

def pre_info(json_path):
    json_dict=_parse_json(json_path)
    img_list=json_dict["images"]
    img_name_list=[]
    img_ann_list=[]
    for item in img_list:
        img_name_list.append(item["img_name"])
        temp_nail_list=[]
        for pre_item in item["pre"]:
            if len(pre_item.keys())==2:
                temp_nail_list.append((pre_item["rec"],pre_item["kps"]))
        img_ann_list.append(temp_nail_list)
    return img_name_list,img_ann_list

def _xywh_to_xyxy(xywh_list):
    return [xywh_list[0],xywh_list[1],xywh_list[0]+xywh_list[2],xywh_list[1]+xywh_list[3]]

def compare_ious(pre_ann,gt_ann,gt_shapes,low_iou_count,zero_iou_count):
    "compare iou and return normlized kps-pair of pre and gt"
    # num_recs=len(pre_ann)
    # width=gt_shapes[0]
    low_iou_flag = False
    pre_ann=np.array(pre_ann)
    gt_ann=np.array(gt_ann)
    pre_ann_recs=pre_ann[:,0].tolist()
    gt_ann_recs=gt_ann[:,0].tolist()
    pre_ann_kps=pre_ann[:,1].tolist()
    gt_ann_kps=gt_ann[:,1].tolist()
    kps_list=[]
    #for test
    raw_kps_list=[]
    low_iou_rec_list = []
    for reci in range(len(pre_ann_recs)):
        iou_list=[]
        width_list = []
        pre_ann_rec = []
        iou_value = -1.0
        for x in pre_ann_recs[reci].split(" "):
            pre_ann_rec.append(float(x))
        for recj in range(len(gt_ann_recs)):
            # print('pre_reci:', recj)
            # pre_reci=[ x for x in pre_ann_recs[reci]]
            # gt_recj=[int(x) for x in gt_ann_recs[recj]]
            # print(pre_ann_recs)
            # print(gt_ann_recs)
            # pre_ann_rec = [float(x) for x in pre_ann_recs[reci].split(" ")]
            # low_iou_pre_rec =pre_ann_rec
            # print(pre_ann_rec,"<==>",gt_ann_recs[recj])
            width_list.append(gt_ann_recs[recj][2])
            gt_to_xyxy_list=_xywh_to_xyxy(gt_ann_recs[recj])
            iou_value=_compute_iou(pre_ann_rec,gt_to_xyxy_list)
            # print(iou_value)
            iou_list.append(iou_value)
        # print(max(iou_list))
        this_index = iou_list.index(max(iou_list))
        if max(iou_list) < 0.5:
            low_iou_flag = True
            low_iou_count+=1
            if max(iou_list)==0:
                zero_iou_count+=1
            #
            # print(pre_ann_rec)
            # print(iou_value)
            low_iou_rec_list.append([pre_ann_rec,gt_ann_recs[this_index]])
            continue
        # rec_width=abs(gt_ann_recs[this_index][2]-gt_ann_recs[this_index][0])
        rec_width = width_list[this_index]
        # print("rec_width====>",rec_width)
        pre_ann_kp=[float(x) for x in pre_ann_kps[reci].split(" ")]
        norm_pre_kps=[float(x)/float(rec_width) for x in pre_ann_kp]
        # print(norm_pre_kps)
        norm_gt_kps=[float(x)/float(rec_width) for x in gt_ann_kps[this_index]]
        kps_list.append((norm_pre_kps,norm_gt_kps))
        raw_kps_list.append((pre_ann_kp,gt_ann_kps[this_index]))
    return kps_list,raw_kps_list,low_iou_count,low_iou_flag,low_iou_rec_list,gt_ann_recs,zero_iou_count

def create_compare_pair(pre_json_path,gt_json_list):
    pre_img_names,pre_anns=pre_info(pre_json_path)
    gt_img_names,gt_img_shapes,gt_anns=combine_all_name_list(gt_json_list)
    all_kps_pair=[]
    #for test
    all_raw_kps_list=[]
    low_iou_count=0
    zero_iou_count = 0
    low_iou_name = []
    all_low_iou_imgs_list = []
    low_iou_all_gts = []
    for i in range(len(pre_img_names)):
        # name="/".join(pre_img_names[i].split("/")[-2:])
        name = pre_img_names[i]
        if pre_img_names[i].startswith("bg"):
            print(pre_img_names)
            continue
        if name in gt_img_names:
            gt_i=gt_img_names.index(name)
        else:
            # print(name)
            continue
        pre_ann=pre_anns[i]
        gt_ann=gt_anns[gt_i]
        gt_shape=gt_img_shapes[gt_i]
        # print("gt_ann传入前",gt_ann)
        # single_kps_pair,raw_kps_list=compare_ious(pre_ann,gt_ann,gt_shape)
        single_kps_pair, raw_kps_list,low_iou_count,low_iou_flag,single_img_low_iou_rec_list, low_iou_all_gts_return,zero_iou_count = compare_ious(pre_ann, gt_ann, gt_shape,low_iou_count,zero_iou_count)
        if low_iou_flag:
            low_iou_name.append(pre_img_names[i])
            all_low_iou_imgs_list.append(single_img_low_iou_rec_list)
            low_iou_all_gts.append(low_iou_all_gts_return)
        # print(name)
        all_kps_pair.extend(single_kps_pair)
        all_raw_kps_list.extend(raw_kps_list)
    print("low_iou_count:",low_iou_count)
    print("zero_iou_count:",zero_iou_count)
    return all_kps_pair,all_raw_kps_list,low_iou_name,all_low_iou_imgs_list,low_iou_all_gts

def compute_std(list1,list2):
    "list1 and list2 should have the same length"
    array_1 =np.array(list1)
    array_2=np.array(list2)
    if array_1.shape!=array_2.shape:
        print("shape error!")
    sqrt_sum=0
    for i in range(0,array_1.shape[0],2):
        x_pre=array_1[i]
        y_pre=array_1[i+1]
        x_gt=array_2[i]
        y_gt=array_2[i+1]
        one_point_sqr=np.sqrt(np.square(x_gt-x_pre)+np.square(y_gt-y_pre))
        sqrt_sum+=one_point_sqr
    return sqrt_sum/16.0

def compute_std_ori(list1,list2):
    "list1 and list2 should have the same length"
    array_1 =np.array(list1)
    array_2=np.array(list2)
    if array_1.shape!=array_2.shape:
        print("shape error!")
    sqrt_sum=0
    for i in range(0,array_1.shape[0],2):
        x_pre=array_1[i]
        y_pre=array_1[i+1]
        x_gt=array_2[i]
        y_gt=array_2[i+1]
        one_point_sqr=np.sqrt(np.square(x_gt-x_pre)+np.square(y_gt-y_pre))
        sqrt_sum+=one_point_sqr
    return sqrt_sum/16.0


def evalution(pre_json_path,gt_json_list,result_txt_path,txt_path=None):
    if txt_path:
        _,gt_json_list=parse_pred_txt(txt_path)
    all_kps_pair,all_raw_test_gt_list,low_iou_img_name,all_low_iou_img_rect_list, low_iou_all_gts= create_compare_pair(pre_json_path,gt_json_list)
    model_name = result_txt_path.split("/")[-1][7:-4]
    vis_dir = "/media/SENSETIME\wangpengju/data/vis/vis_"+model_name
    _copy_vis_img(low_iou_img_name,all_low_iou_img_rect_list,low_iou_all_gts,vis_dir)
    nail_count=0
    nail_sqrt_sum=0
    max_loss=0
    max_cout=0
    for i in range(len(all_kps_pair)):
        kps_pair_pre,kps_pair_gt=all_kps_pair[i]

        #for test
        # print('all_raw_test_gt_list[i]',all_raw_test_gt_list[i])
        # raw_kps_pair_pre,raw_kps_pair_gt=all_raw_test_gt_list[i]


        # print("======================")
        # print(kps_pair_pre)
        # print(kps_pair_gt)
        # print("======================")
        # print(kps_pair_pre)
        # print(kps_pair_gt)
        if len(kps_pair_gt)!=len(kps_pair_pre):
            print("size error")
            # print(kps_pair_pre,"<===>",kps_pair_gt)
            continue
        one_nail_sqrt=compute_std(kps_pair_pre,kps_pair_gt)
        # if one_nail_sqrt>0.8:
        #     print(one_nail_sqrt)
        #     print("pre原数据：",raw_kps_pair_pre)
        #     print("原数据：",raw_kps_pair_gt)
        #     print("pre_pair数据：",kps_pair_pre)
        #     print("gt_pair数据：",kps_pair_gt)
        # if one_nail_sqrt>0.08:
        #     max_cout+=1
        #     continue
        # print(max_cout)
        nail_sqrt_sum+=one_nail_sqrt
        nail_count+=1
    with open("low_iou_name_log.txt",'a') as f:
        localtime = time.asctime(time.localtime(time.time()))
        f.write("======================\n")
        f.write("model_name:"+result_txt_path.split("/")[-1][7:]+".model\n")
        f.write("time:"+localtime+"\n")
        f.write("nail_count:"+str(nail_count)+"\n")
        f.write("pandiu+low_iou_count:"+str(3993-nail_count)+"\n")
        f.write("评估结果："+str(nail_sqrt_sum/nail_count)+"\n")
        for item in low_iou_img_name:
            f.write(item+"\n")
        f.write("======================\n")
    print(low_iou_img_name[:10])
    print("max_count",max_cout)
    print("nail_count:",nail_count)
    print("pandiu+low_iou_count:",3993-nail_count)
    print("评估结果：",nail_sqrt_sum/nail_count)
    return nail_sqrt_sum/nail_count


def _get_gt(json_path):
    "parse ground truth txt and return the image name list of gt"
    json_dict=_parse_json(json_path)
    img_list=json_dict["images"]
    ann_list=json_dict["annotations"]
    img_name_list=[]
    img_id_list=[]
    img_shape_list=[]
    img_ann_list=[]
    for item in img_list:
        img_name=json_path.split("/")[-3]+"/images/"+item["file_name"]
        img_id=item["id"]
        img_xy=(item["width"],item["height"])
        img_name_list.append(img_name)
        img_id_list.append(img_id)
        img_shape_list.append(img_xy)

    for i in range(len(img_id_list)):
        temp_ann_list=[]
        # print(i)
        for item in ann_list:
            # if item["image_id"]==11555:
            #     print("11555")
            if item["image_id"]==img_id_list[i]:
                # print("{}_{}_{}".format(i,item["image_id"],img_id_list[i]))
                kp_list=item["keypoints"]
                kp_list_no_conf=[]
                for j in range(0,len(kp_list),3):
                    kp_list_no_conf.append(kp_list[j])
                    kp_list_no_conf.append(kp_list[j+1])
                temp_ann_list.append((item["bbox"],kp_list_no_conf))

        img_ann_list.append(temp_ann_list)
        # print("temp:",len(temp_ann_list))
        # print("temp:", temp_ann_list)
    return img_name_list,img_shape_list,img_ann_list


def combine_all_name_list(file_path_list):
    "join all name_list of given. "
    all_names=[]
    all_shapes=[]
    all_anns=[]
    for item in file_path_list:
        names,shpes,anns=_get_gt(item)
        all_names.extend(names)
        all_shapes.extend(shpes)
        all_anns.extend(anns)
    return all_names,all_shapes,all_anns


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


def intersect_list():
    "get the two list intersection of two given list."
    pass

def copy_image(pred_txt,image_root,tar_root):
    name_list,_=parse_pred_txt(pred_txt)
    for name in name_list:
        # print(name)
        img_path=os.path.join(image_root,name)
        sub_dir="/".join(name.split("/")[:-1])
        tar_dir=os.path.join(tar_root,sub_dir)
        if not os.path.exists(tar_dir):
            os.makedirs(tar_dir)
        tar_path=os.path.join(tar_root,name)
        if not os.path.exists(img_path):
            print(img_path)
            continue
        copyfile(img_path,tar_path)

def _draw_rectangle(img ,pt1,pt2,color = None,linetype= None):
    # if linetype:
    #     img = cv2.rectangle(img,pt1,pt2,color,thickness=1,lineType=linetype)
    # else:
    #     img = cv2.rectangle(img, pt1, pt2, color, thickness=1)
    img = cv2.rectangle(img, pt1, pt2, color, thickness=3)
    return img

def _copy_vis_img(low_iou_name_list,all_low_iou_img_rect_list,low_iou_all_gts,vis_dir="vis"):
    for i in range(len(low_iou_name_list)):
        ori_path = os.path.join(vis_dir,low_iou_name_list[i])
        img = cv2.imread(ori_path)
        single_image_recs = all_low_iou_img_rect_list[i]
        for gt in low_iou_all_gts[i]:
            gt_new = _xywh_to_xyxy(gt)
            img = _draw_rectangle(img, (int(gt_new[0]), int(gt_new[1])), (int(gt_new[2]), int(gt_new[3])),(127, 127, 127))
        for rec in single_image_recs:
            pre_rec,gt_rec = rec
            #pre_rec_transform =_xywh_to_xyxy(pre_rec)  #本身就是xyxy格式，不需要轉換
            gt_rec_transform =_xywh_to_xyxy(gt_rec)
            # if low_iou_name_list[i]=="doublehand_nails_test/images/lilin/lilin_1_10.jpg":
            #     print("gt_rec==>",gt_rec)
            #     print("pre_rec==>",pre_rec)
            #     break
            img = _draw_rectangle(img,(int(pre_rec[0]),int(pre_rec[1])),(int(pre_rec[2]),int(pre_rec[3])),(0,255,0))
            img = _draw_rectangle(img,(int(gt_rec_transform[0]),int(gt_rec_transform[1])),(int(gt_rec_transform[2]),int(gt_rec_transform[3])),color=(0,0,255))
        tar_root = vis_dir+"_low_iou"
        tar_path = os.path.join(tar_root,low_iou_name_list[i])
        if not os.path.exists(os.path.dirname(tar_path)):
            os.makedirs(os.path.dirname(tar_path))
        #copyfile(ori_path,tar_path)
        cv2.imwrite(tar_path,img)

def parse_pred_txt(path_txt):
    "parse the pred txt and find all image_names who have pred_result,the return the pred_list and pred_result"
    list_for_save=[]
    index1=0
    name_list=[]
    with open(path_txt,"r") as f:
        items=f.readlines()
    for i in range(len(items)):
        if str(items[i]).strip().endswith("jpg") or str(items[i]).strip().endswith('png') or len(str(items[i]).split("/"))>1:
            if index1==0:
                index1=i
            distance=i-index1
            if distance>5:
                # print('items[index1]:',items[index1])
                list_for_save.append(str(items[index1]).strip().replace("\n",""))
                name_list.append(str(items[index1]).strip().replace("\n",""))
                list_for_save.extend(items[index1+3:i-2])
                # data_len=i-index1-5
            index1=i
    # print(list_for_save)
    json_file=json_formt(list_for_save)
    with open("test.json","w") as f:
       f.write(json_file)
    return name_list,json.loads(json_file)





if __name__ == '__main__':
    txt_path=sys.argv[1]
    test_path="{}".format(txt_path)
    img_root="/home/SENSETIME/wangpengju/github/data/heatmap"
    tar_img_root="/home/SENSETIME/wangpengju/github/data/heatmap_fc"
    if not os.path.exists(tar_img_root):
        os.makedirs(tar_img_root)
    copy_image(test_path,img_root,tar_img_root)

#for evalution

    # gt_json_list=["/home/SENSETIME/wangpengju/github/data/tracking_data_test/doublehand_nails_test/images/nail_shape_kps_test.json",
    #               "/home/SENSETIME/wangpengju/github/data/tracking_data_test/gel_nails_test/images/nail_shape_kps_test.json",
    #               "/home/SENSETIME/wangpengju/github/data/tracking_data_test/nails_data_test/images/nail_shape_kps_test_v2.json",
    #               "/home/SENSETIME/wangpengju/github/data/tracking_data_test/nails_data_test/images/nail_shape_kps_test.json"]
    gt_json_list=["/home/SENSETIME/wangpengju/github/data/tracking_data_test/doublehand_nails_test/images/nail_shape_kps_test.json",
                  "/home/SENSETIME/wangpengju/github/data/tracking_data_test/gel_nails_test/images/nail_shape_kps_test.json",
                  "/home/SENSETIME/wangpengju/github/data/tracking_data_test/nails_data_test/images/nail_shape_kps_test_v2.json"]
    # gt_json_list = ["/home/SENSETIME/wangpengju/github/data/heatmap_newdata/data_nail_20210527/images/nail_shape_kps_test.json"]
    pre_json="/home/SENSETIME/wangpengju/PycharmProjects/pythonProject/test_nail_model/test.json"
    # pre_json = "/home/SENSETIME/wangpengju/PycharmProjects/pythonProject/test_nail_model/pred_hm_fc _test.json"
    evalution(pre_json,gt_json_list,txt_path)
    # test()