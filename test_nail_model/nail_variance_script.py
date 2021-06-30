import os

if __name__ == '__main__':
    model_list=['M_Nails_Alignment_1.4.0_sketch.model']
    mode='sync'
    #mode='async_deadline'
    smooth_factor=0.8
    for item in model_list:
        print("model_name==>",item)
        baseline="python nail_variance.py {} {} {}".format(item[:-6],mode,smooth_factor)
        os.system(baseline)
    print("测试完成！！！")