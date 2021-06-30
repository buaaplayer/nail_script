import cv2
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
def _xywh_to_xyxy(xywh_list):
    return [xywh_list[0],xywh_list[1],xywh_list[0]+xywh_list[2],xywh_list[1]+xywh_list[3]]


def compare_iou(gt_list,pre):
    img = cv2.imread("lilin_1_10.jpg")
    for item in gt_list:
        new_item = _xywh_to_xyxy(item)
        new_img = _draw_rectangle(img,(int(new_item[0]),int(new_item[1])),(int(new_item[2]),int(new_item[3])))
        new_img = _draw_rectangle(new_img,(int(pre[0]),int(pre[1])),(int(pre[2]),int(pre[3])),color=(0,0,255))
        cv2.imwrite("test.jpg",new_img)
        iou_value = _compute_iou(new_item,pre)
        print(iou_value)

def _draw_rectangle(img ,pt1,pt2,color = (127,127,127),linetype= None):
    img = cv2.rectangle(img, pt1, pt2, color, thickness=3)
    return img






if __name__ == '__main__':
    gt_list = [[761.21644, 536.07619, 45.19605, 65.62714],
[748.83396, 593.03561, 47.67255, 65.62714],
[1091.93954, 705.94458, 63.92947, 74.81108],
[1076.97732, 769.87405, 76.17128, 53.04785],
[1159.94962, 715.46599, 74.81108, 78.89168],
[1205.92485, 650.57467, 68.48156, 73.96009],
[1106.3983, 908.97846, 69.39465, 58.43761],
[1253.59054, 502.91621, 63.00305, 65.74231],
[1034.44952, 1015.15836, 63.91613, 52.04599]]
    pre=[1134.0, 843.0, 1198.0, 891.0]
    compare_iou(gt_list,pre)