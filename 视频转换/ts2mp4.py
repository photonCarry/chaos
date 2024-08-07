# coding=UTF-8
import os
import json
from shutil import copyfile

exts = [".ts", ".mkv", ".avi", ".wmv", ".flv", ".webm"]

def getInfo(file):
    p = os.popen('ffprobe -select_streams v -show_entries\
              format=duration,size,bit_rate,filename\
              -show_streams -v quiet -of csv="p=0" -of json -i "' + file + '"')
    info = json.loads(p.buffer.read().decode(encoding='utf8'))
    return info

global logf
logf = open('app.log', 'a', encoding='utf-8')

def trans(inn, out, ext):
    global logf

    try:
        info = getInfo(inn)
        width = info['streams'][0]['width']
        height = info['streams'][0]['height']

        if (width >= height and width <= 480) or (width < height and width <= 240):
            if ext == '.mp4':
                copyfile(inn, out)
                print('copy', inn, out)
                logf.write('[INFO] copy ' + inn + " " + out + '\n')
                return
            
        w = 'min(480,iw)'
        if width < height:
            w = 'min(240,iw)'
        h = '-2'
        strcmd = 'ffmpeg -i "' + inn + '" -vf "scale=\'' + w + '\':' + h + '" "' + out + '"'
        print(strcmd)
        if os.system(strcmd) != 0:
            print('[FAILED]', strcmd)
            logf.write('[FAILED] ' + strcmd + '\n')
    except Exception as e:
        print('[PANIC]', inn, e)
        logf.write('[PANIC] ' + inn + '\n')
        logf.write('[PANIC] ' + e + '\n')

def downmp4(tsPath, mp4Path, f, ext):
    inn = r"" + tsPath + "\\" + f
    out = r"" + mp4Path + "\\" + os.path.splitext(f)[0] + "_down.mp4"
    if os.path.exists(out):
        print('skip downed', out)
        return
    trans(inn, out, ext)

def ts2mp4(tsPath, mp4Path):
    print('do video -> mp4 transform', tsPath, mp4Path)
    files = os.listdir(tsPath)
    for f in files:
        if os.path.isdir(f):
            continue

        doit = False
        ext = os.path.os.path.splitext(f)[1].lower()
        if ext == ".mp4":
            downmp4(tsPath, mp4Path, f, ext)
            continue

        if ext == '.mp4' or ext == '.py' or ext == '.log':
            continue
        for e in exts:
            if ext == e:
                doit = True
                break
        if not doit:
            print('skip unknown file', f)
            continue
        inn = r"" + tsPath + "\\" + f
        out = r"" + mp4Path + "\\" + os.path.splitext(f)[0] + ".mp4"
        if os.path.exists(out):
            print('skip transed', out,)
            continue
        # print('why', inn, out)
        trans(inn, out, ext)

# 旋转
# ffmpeg -i abc.mp4 -vf "transpose=1" abc-90.mp4

if __name__ == '__main__':
    pwd = os.getcwd()
    ts2mp4(pwd, pwd + "\\out")
    logf.close()