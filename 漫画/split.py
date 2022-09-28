import cv2
import os,sys
import numpy as np


def imgchuli(file, filename, filetype):
    data = np.fromfile(file, dtype=np.uint8)  # 先用numpy把图片文件存入内存：data，把图片数据看做是纯字节数据
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 从内存数据读入图片

    h = int(img.shape[0])
    w = int(img.shape[1])
    if w < 2000:
        return

    img1 = img[0:h, int(w / 2):]
    img2 = img[0:h, 0:int(w / 2)]

    basename = os.path.splitext(file)[0]  # 文件名
    f1 = basename + '_01' + filetype
    f2 = basename + '_02' + filetype
    cv2.imencode('.' + filetype, img1)[1].tofile(f1)
    cv2.imencode('.' + filetype, img2)[1].tofile(f2)
    os.remove(file)


def fenge(path_name):
    filetype_list = ['.jpg', '.png', '.JPG']

    if path_name == '':
        return

    file_list = os.listdir(path_name)  # 该文件夹下所有的文件（包括文件夹）

    for file in file_list:  # 遍历所有文件
        fullname = os.path.join(path_name, file)
        if os.path.isdir(fullname):  # 如果是文件夹则跳过
            print('do dir', file)
            fenge(fullname)
            continue

        filename = os.path.splitext(file)[0]  # 文件名
        filetype = os.path.splitext(file)[1]  # 文件扩展名

        if filetype in filetype_list:
            print('do file', file)
            imgchuli(fullname, filename, filetype)
        else:
            print('skip file', file)

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 1:
        print('请输入路径')
        sys.exit()
    path_name = sys.argv[1]
    fenge(path_name)



