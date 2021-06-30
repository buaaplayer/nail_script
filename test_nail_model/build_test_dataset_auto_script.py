import os
import time
import datetime



if __name__ == '__main__':
    date_today=datetime.date.today()
    date_dir="".join(str(date_today).split("-"))
    # print(date_dir)
    txt_dir="/home/SENSETIME/wangpengju/github/data/tracking_data_test/{}/image".format(date_dir)
    txt_list=os.listdir(txt_dir)
    #txt_list=[]
    command_line="python build_test_dataset_for_auto_use.py {}"
    for item in txt_list:
        if not item.endswith(".txt"):
            continue
        if item.startswith("video"):
            continue
        print("========================================================")
        print("item==>",item)
        txt_path=os.path.join(txt_dir,item)
        os.system(command_line.format(txt_path))
