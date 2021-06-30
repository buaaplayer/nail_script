import os
import datetime

if __name__ == '__main__':
    """
    in this location, you have two choises , give the model list or the model_dir
    """
    # model_list=['rpn_nobn_kp200w_pd200w_kpgtx2.caffemodel',
    #             'rpn_nobn_kp200w_pd200w_kpgt+100.caffemodel',
    #             'nobn_kp200w_pd200w_pdlw1_new.caffemodel']    #1/2
    model_dir="/home/SENSETIME/wangpengju/github/modelS/0629/sketch/packing_models"
    model_list=os.listdir(model_dir) #2/2
    date_today = datetime.date.today()
    date_dir = "".join(str(date_today).split("-"))
    txt_dir="/home/SENSETIME/wangpengju/github/data/tracking_data_test/{}/video".format(date_dir)
    mode='sync'
    #mode='async_deadline'
    smooth_factor_list=[0.0,0.2,0.4,0.6,0.8]
    for item in model_list:
        print("<======================================>")
        print("model_name==>",item)
        for sf in smooth_factor_list:
            print("smooth_factor==>",sf)
            baseline="python nail_variance.py {} {} {} {}".format(txt_dir,item[:-6],mode,sf)
            os.system(baseline)
    print("测试完成！！！")