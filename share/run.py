# !/usr/bin/env python
# -*- coding:UTF-8 -*-
import os
import sys
import webbrowser
import time
import random
import subprocess
import datetime
import paramiko

SAMPLE_NAME = 'sample.txt'
SHARE_PATH = 'C:\\share\\'
SAMPLE_PATH = SHARE_PATH + SAMPLE_NAME

def open_web(app, url):
    if app == 'chrome':
        app_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    elif app == 'firefox':
        app_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    elif app == 'ie':
        app_path = 'C:\\Program Files\\Internet Explorer\\iexplore.exe'
    subprocess.Popen(app_path + ' ' + url)

def open_pdf(app, name):
    if app == 'adobe':
        app_path = 'C:\\Program Files\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe'
    elif app == 'foxit':
        app_path = 'C:\\Program Files\\Foxit Software\\Foxit Reader\\FoxitReader.exe'
    subprocess.Popen(app_path + ' ' + SHARE_PATH + 'pdf\\' + name)

def open_doc(name, f):
    app_path = 'C:\\Program Files\\Kingsoft\\WPS Office\\10.8.0.6206\\office6\\wps.exe'
    subprocess.Popen(app_path + ' ' + SHARE_PATH + 'doc\\' + name)

def open_ppt(name, f):
    app_path = 'C:\\Program Files\\Kingsoft\\WPS Office\\10.8.0.6206\\office6\\wpp.exe'
    subprocess.Popen(app_path + ' ' + SHARE_PATH + 'ppt\\' + name)

def open_xls(name, f):
    app_path = 'C:\\Program Files\\Kingsoft\\WPS Office\\10.8.0.6206\\office6\\et.exe'
    subprocess.Popen(app_path + ' ' + SHARE_PATH + 'xls\\' + name)

def open_app(app, f):
    try:
        subprocess.Popen(app)
        f.writelines('[' + get_time() + ']\tapp\t' + app + '\n')
    except:
        f.writelines('error ' + app + '\n')

def open_pic(pic, f):
    try:
        #subprocess.Popen('C:\\Program Files\\Meitu\\KanKan\\KanKan.exe ' + SHARE_PATH + '\\pic\\' + pic)
        subprocess.Popen('mspaint ' + SHARE_PATH + '\\pic\\' + pic)
        f.writelines('[' + get_time() + ']\tpic\t' + pic + '\n')
    except:
        f.writelines('error ' + pic + '\n')

def benchmark():
    time.sleep(300)
    os.system('stress-ng --cpu 4 --vm 2 --hdd 1 --fork 8 --switch 4 --timeout 5m --metrics-brief')

def download_list():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('biocluster.ucr.edu', username='wsong008', password='cl3412CL@er')
    sftp = ssh.open_sftp()
    sftp.get('/rhome/wsong008/bigdata/vm_mem_dump_tool/share/' + SAMPLE_NAME, SAMPLE_PATH)
    sftp.close()
    ssh.close()

def upload_result():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('biocluster.ucr.edu', username='wsong008', password='cl3412CL@er')
    sftp = ssh.open_sftp()
    sftp.put(SAMPLE_PATH, '/rhome/wsong008/bigdata/vm_mem_dump_tool/share/result_' + SAMPLE_NAME)
    sftp.close()
    ssh.close()

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    download_list()
    #while (os.path.exists(SAMPLE_PATH) == False):
    #    time.sleep(2)
    result = []
    f = open(SAMPLE_PATH, 'r')
    for line in f:
        if '\t' not in line or 'internal log' in line:
            break
        if (len(line) != 0):
            result.append(line.strip())
    f.close()
    #print result
    log = []
    bufsize = 0
    f = open(SAMPLE_PATH, 'ab', bufsize)
    f.writelines('\n---------internal log---------\n\n')
    for line in result:
        print line
        s = line.split('\t')
        if (s[0] == 'foxit' or s[0] == 'adobe'):
            open_pdf(s[0], s[1])
            f.writelines('[' + get_time() + ']\t' + s[0] + '\t' + s[1] + '\n')
        elif (s[0] == 'ie' or s[0] == 'firefox' or s[0] == 'chrome'):
            open_web(s[0], s[1])
            f.writelines('[' + get_time() + ']\t' + s[0] + '\t' + s[1] + '\n')
        elif (s[0] == 'app'):
            open_app(s[1], f)
        elif (s[0] == 'pic'):
            open_pic(s[1], f)
        elif (s[0] == 'doc'):
            open_doc(s[1], f)
        elif (s[0] == 'ppt'):
            open_ppt(s[1], f)
        elif (s[0] == 'xls'):
            open_xls(s[1], f)
        time.sleep(random.randint(1, 3))
    f.close()
    upload_result()

if __name__ == '__main__':
    main()
