import cv2 as cv



def draw_boxes(img,boxes,color=(0,255,0),name=None):
    for box in boxes:
        print(box)
        # point1=(int(float(str(box[0]))),int(float(str(box[1]))))
        # point2=(int(float(str(box[2]))),int(float(str(box[3]))))
        # cv.rectangle(img,point1,point2,(255,0,0),5,2)
        point1=(int(box[0]),int(box[1]))
        point2=(int(box[2]),int(box[3]))
        cv.rectangle(img, point1, point2, color, 5, 2)
    return img



def draw_box(img,box,color='red',name=None):
    cv.rectangle(img,(box[0],box[1]),(box[2],box[3]),color,5,2,4)
    return img


#解析txt文件，for test
def parse_boxes_file(file_path):
    video_boxes={}
    frame_boxes = []
    frame_id=0
    with open(file_path,"r") as f:
        line_items=f.readlines()
        for line_item in line_items:
            line_item=line_item.strip().split(",")
            if len(line_item)==1:
                video_boxes[frame_id] = frame_boxes
                frame_id=int(line_item[0])
                frame_boxes =[]
            elif len(line_item)==4:
                # box=line_item
                frame_boxes.append(line_item)
            else:
                print("data wrong!!!")
    # print(video_boxes)
    return video_boxes


def read_video(video_path,boxes_file_path):
    #
    # video_boxes={}
    # frame_boxes=None
    cap=cv.VideoCapture(video_path)
    if cap.isOpened():
        print("视频正常打开！")
    else:
        print("视频无法正常打开!")
    fps = cap.get(cv.CAP_PROP_FPS)  # 返回视频的fps--帧率
    width = cap.get(cv.CAP_PROP_FRAME_WIDTH)  # 返回视频的宽
    height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # 返回视频的高
    fourcc=cv.VideoWriter_fourcc(*'XVID')
    out=cv.VideoWriter("out.avi",fourcc,fps,(int(width),int(height)))
    ret,frame=cap.read()
    frame_id=0
    while ret:
        # frame_copy=frame
        video_boxes=parse_boxes_file(boxes_file_path)
        frame_boxes=video_boxes[frame_id]
        img=draw_boxes(frame,frame_boxes)
        if frame_id>7:
            p2_id=frame_id-8
            p_frame_boxes=video_boxes[p2_id]
            img=draw_boxes(img,p_frame_boxes,color=(0,0,255))
        out.write(img)
        cv.imshow("test",img)
        if cv.waitKey(20)==27:
            break
        ret, frame = cap.read()
        frame_id+=1
    out.release()



if __name__ == '__main__':
    # video_path="/home/SENSETIME/wangpengju/github/sdk_hand_arface/install/linux-x86_64/release/samples/hand/demo_for_test.avi"
    video_path = "/home/SENSETIME/wangpengju/github/sdk_hand_arface/install/linux-x86_64/release/samples/hand/ori.m4v"
    boxes_file_path="/home/SENSETIME/wangpengju/github/sdk_hand_arface/install/linux-x86_64/release/samples/hand/test.txt"
    # parse_boxes_file(boxes_file_path)
    read_video(video_path,boxes_file_path)