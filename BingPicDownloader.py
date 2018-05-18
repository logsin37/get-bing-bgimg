# coding:utf8
# 环境要求:python2.7x,PIL,pywin32
# 备注:只在win7系统试过正常
# 创建时间:2015-1

from PIL import Image
import win32api
import win32con
import win32gui
import re
import os
import time
import urllib.request


class BingPicDownloader:

    def __init__(self):
        self.content = urllib.request.urlopen('http://cn.bing.com/').read()
        self.bgImageUrl = ''
        self.localFileName = ''
        self.localBMPFileName = ''

    def parserImageURL(self):
        reg = re.compile(r'g_img={url: "(.*?jpg)"')
        data = self.content.decode('utf-8')
        partialBgImageUrl = reg.findall(data) # like ['/az/hprichbg/rb/FalcoPeregrinus_ZH-CN12522703608_1920x1080.jpg']
        print(partialBgImageUrl)
        self.bgImageUrl = [url for url in map(lambda partial : 'http://cn.bing.com' + partial, partialBgImageUrl)];
        # github上的开源地址
        # self.bgImageUrl = ['https://bing.ioliu.cn/v1?d=0&w=1366&h=768']

    def createLocalFileName(self):
        path = 'D:/MyPrograms/BingPicDownloader/pic/'
        if not os.path.exists(path):
            os.mkdir(path)
        randomStr = time.strftime("%Y%m%d", time.localtime())
        self.localFileName = path + randomStr + '.jpg'
        self.localBMPFileName = path + randomStr + '.bmp'

    def downloadImage(self):
        if self.bgImageUrl == '':
            self.parserImageURL()
        if self.localFileName == '':
            self.createLocalFileName()
        path = self.bgImageUrl[0].replace('\\', '')
        print(path)
        urllib.request.urlretrieve(path, self.localFileName)

    def setWallpaperFromBmp(self):
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, os.path.realpath(self.localBMPFileName), 1 + 2)  

    def setWallpaper(self):
        # 把图片格式统一转换成bmp格式,并放在源图片的同一目录
        bmpImage = Image.open(self.localFileName)
        bmpImage.save(self.localBMPFileName, "BMP")
        os.remove(self.localFileName)  
        self.setWallpaperFromBmp()


if __name__ == '__main__':
    bingPicDownloader = BingPicDownloader()
    bingPicDownloader.downloadImage()
    bingPicDownloader.setWallpaper()
