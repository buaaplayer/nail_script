import os


def test(item_path,name,model_dir):
    # import pdb
    # pdb.set_trace()
    # os.system("cd {}".format(model_dir))
    os.system("cp {} ./rotate/model.bin".format(item_path))
    os.system("sh compact.sh {}".format(name))
    # os.system("")





if __name__ == '__main__':
    model_dir='/home/SENSETIME/wangpengju/github/modelS/one_tests/nail_track'
    iters_dir='/home/SENSETIME/wangpengju/github/modelS/one_tests_iters'
    test_item='nobn_iter_10w_kp200w.caffemodel'
    test_path='/home/SENSETIME/wangpengju/github/modelS/one_tests_iters/nobn_iter_10w_kp200w.caffemodel'
    iters=os.listdir(iters_dir)
    # for item in iters:
    #     item_path=os.path.join(iters_dir,ite)
    #     test(item_path,item,model_dir)
    test(test_path, test_item, model_dir)
