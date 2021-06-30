import json
import numpy as np

def _parse_json(json_path):
    with open(json_path,"r") as f:
        return json.load(f)

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

def compute_ann_rec(gt_ann):
    gt_ann_np = np.array(gt_ann)
    # print(gt_ann_np)
    gt_ann_recs = gt_ann_np[:, 0].tolist()
    sum_w=0
    sum_h=0
    min_w = 10000
    min_h = 10000
    count_small_nail = 0
    for gt_ann_rec in gt_ann_recs:
        sum_w+=gt_ann_rec[2]
        sum_h+=gt_ann_rec[3]
        t = max(min_w,min_h)
        if max(gt_ann_rec[2],gt_ann_rec[3])<90:
            count_small_nail +=1
        if gt_ann_rec[2]<t and gt_ann_rec[3]<t:
            min_w = gt_ann_rec[2]
            min_h = gt_ann_rec[3]

    return sum_w*1.0/len(gt_ann_recs),sum_h*1.0/len(gt_ann_recs),min_w,min_h,count_small_nail,len(gt_ann_recs),sum_w,sum_h


def test(gt_json_list):
    gt_img_names, gt_img_shapes, gt_anns = combine_all_name_list(gt_json_list)
    #针对每张图片平均值求和
    sum_w=0
    sum_h=0
    #all sum,用于整体求和
    all_sum_w = 0
    all_sum_h = 0
    #--------------
    all_min_w = 10000
    all_min_h = 10000
    all_count_small_nail=0
    all_gt_rec_num=0
    for i in range(len(gt_anns)):
        if len(gt_anns[i])==0:
            print("empty gt error!")
            print('gt_img_names==>',gt_img_names[i])
            continue
        w_avg,h_avg,min_w,min_h,count_small_nail,len_gt_ann_recs,sum_w_per_img,sum_h_per_img = compute_ann_rec(gt_anns[i])
        sum_w+=w_avg
        sum_h+=h_avg
        all_sum_w+= sum_w_per_img
        all_sum_h += sum_h_per_img
        all_count_small_nail+=count_small_nail
        all_gt_rec_num+=len_gt_ann_recs
        t1=max(all_min_w,all_min_h)
        t2= max(min_w,min_h)
        if t2<t1:
            all_min_w = min_w
            all_min_h = min_h
    all_avg_w = sum_w / len(gt_anns)
    all_avg_h = sum_h / len(gt_anns)
    print('all_avg_w==>',all_avg_w)
    print('all_avg_h==>',all_avg_h)
    print('all_min_w==>',all_min_w)
    print('all_min_h==>',all_min_h)
    print('all_count_small_nail==>',all_count_small_nail)
    print('all_gt_rec_num==>',all_gt_rec_num)
    print('entire_average_w==>',all_sum_w/all_gt_rec_num)
    print('entire_average_h==>', all_sum_h / all_gt_rec_num)



if __name__ == '__main__':
    # gt_json_list = [
    #     "/home/SENSETIME/wangpengju/github/data/tracking_data_test/doublehand_nails_test/images/nail_shape_kps_test.json",
    #     "/home/SENSETIME/wangpengju/github/data/tracking_data_test/gel_nails_test/images/nail_shape_kps_test.json",
    #     "/home/SENSETIME/wangpengju/github/data/tracking_data_test/nails_data_test/images/nail_shape_kps_test_v2.json"]
    # gt_json_list=[
    #     '/home/SENSETIME/wangpengju/github2/data/gt_jsons/nail_shape_kps_train.json',
    #     '/home/SENSETIME/wangpengju/github2/data/gt_jsons/nail_shape_kps_train_gel.json',
    #     '/home/SENSETIME/wangpengju/github2/data/gt_jsons/nail_shape_kps_train_v2.json'
    # ]
    gt_json_list =[
        '/home/SENSETIME/wangpengju/github2/data/gt_jsons/nail_shape_kps_train.json',
        '/home/SENSETIME/wangpengju/github2/data/gt_jsons/nail_shape_kps_train_gel.json',
        '/home/SENSETIME/wangpengju/github2/data/gt_jsons/nail_shape_kps_train_v2.json'
    ]

    test(gt_json_list)
