
import requests
        # 1. 在 http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-login.jsp 获取验证码URL
def Downloads_PIC(strPath,strName):
    # 1. 在 http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-login.jsp 获取验证码URL
    url = 'http://www.xxx.com'
    # 2. 以二进制流的方式发送一个Get请求，将stream=True，在读取完左右数据前不断开链接
    rReq = requests.get(url, stream=True)
    # 3. 尝试保存图片
    with open(strPath+strName+'.png', 'wb') as fpPIC:
        # 一次读取1024Byte的内容到byChunk中，如果读取不完则循环读取
        for byChunk in rReq.iter_content(chunk_size=1024):
            if byChunk:
                fpPIC.write(byChunk)
                fpPIC.flush()
        fpPIC.close()

for i in range(1,20+1):
    strFileName = "%03d" % i
    Downloads_PIC('D:/123/123/',strFileName)

import os
import os.path
import random
from PIL import Image,ImageEnhance,ImageFilter

def BinaryzationImg(strImgPath):
    imgOriImg = Image.open(strImgPath)
    pocEnhance = ImageEnhance.Contrast(imgOriImg) # 增加对比度
    imgOriImg = pocEnhance.enhance(2.0) # 增加200%对比度
    pocEnhance = ImageEnhance.Sharpness(imgOriImg) # 锐化
    imgOriImg = pocEnhance.enhance(2.0) # 锐化200%
    pocEnhance = ImageEnhance.Brightness(imgOriImg) # 增加亮度
    imgOriImg = pocEnhance.enhance(2.0) # 增加200%对亮度
    imgGryImg = imgOriImg.convert('L').filter(ImageFilter.DETAIL) # 滤镜效果
    imgBinImg = imgOriImg.convert('1') #转为黑白图片
    #imgBinImg.show()
    return imgBinImg

def ClearNoise(imgBinImg):
    for x in range(1,(imgBinImg.size[0]-1)):
        for y in range(1,(imgBinImg.size[1]-1)):
            # 如果中心点为黑色，周围8点皆为白色，此点为噪点，置为白色
            if imgBinImg.getpixel((x,y))==0 \
                    and imgBinImg.getpixel(((x-1),(y+1)))==255 \
                    and imgBinImg.getpixel(((x-1), y   ))==255 \
                    and imgBinImg.getpixel(((x-1),(y-1)))==255 \
                    and imgBinImg.getpixel(((x+1),(y+1)))==255 \
                    and imgBinImg.getpixel(((x+1), y   ))==255 \
                    and imgBinImg.getpixel(((x+1),(y-1)))==255 \
                    and imgBinImg.getpixel(( x   ,(y+1)))==255 \
                    and imgBinImg.getpixel(( x   ,(y-1)))==255:
                imgBinImg.putpixel([x,y],255) # 此点为噪点，置为白色
    return imgBinImg

def GetCropImgs(imgClrImg):
    ImgList = []
    for i in range(4):
        x = 6 + i*13
        y = 3
        SubImg = imgClrImg.crop((x, y, x+13, y+15))
        ImgList.append(SubImg)
    return ImgList

#
g_Count = 0
strStep1Dir = 'D:/123/step_1'
strStep2Dir = 'D:/123/step_2'
for ParentPath,DirNames,FileNames in os.walk(strStep1Dir):
    for i in FileNames:
        strFullPath = os.path.join(ParentPath,i) # 图片文件路径信息
        imgBinImg = BinaryzationImg(strFullPath)
        imgClrImg = ClearNoise(imgBinImg)
        ImgList = GetCropImgs(imgClrImg)
        for img in ImgList:
            strImgName = "%04d%04d.png" % (g_Count,random.randint(0,9999))
            strImgPath = os.path.join(strStep2Dir,strImgName)
            img.save(strImgPath)
            g_Count += 1

#imgClrImg.show()
#imgBinImg.save('D:/123/123/Binaryzation/1.png')

def GetFeature(imgCropImg):
    nWidth  = 13
    nHeight = 14
    PixelCountList = []
    for y in range(nHeight):
        CountX = 0
        for x in range(nWidth):
            if imgCropImg.getpixel((x, y)) == 0:  # 黑色点
                CountX += 1
        PixelCountList.append(CountX)
    for x in range(nWidth):
        CountY = 0
        for y in range(nHeight):
            if imgCropImg.getpixel((x, y)) == 0:  # 黑色点
                CountY += 1
        PixelCountList.append(CountY)
    return PixelCountList

strMaterialDir = 'D:/123/step_3/6'
strOutDir = 'D:/123/step_4/'
for ParentPath,DirNames,FileNames in os.walk(strMaterialDir):
    with open(strOutDir+'6.txt', 'w') as fpFea:
        for i in FileNames:
            strFullPath = os.path.join(ParentPath,i) # 图片文件路径信息
            imgOriImg = Image.open(strFullPath)
            FeatureList = GetFeature(imgOriImg)
            strFeature = '6 '
            nCount = 1
            for j in FeatureList:
                strFeature = '%s%d:%d ' % (strFeature,nCount,j)
                nCount+=1
            fpFea.write(strFeature+'\n')
            fpFea.flush()
    fpFea.close()


import os
import sys
import os.path
sys.path.append('C:\libsvm-3.21\python')
from PIL import Image,ImageEnhance,ImageFilter
from svmutil import *

def GetFeature(imgCropImg,nImgHeight,nImgWidth):
    PixelCountList = []
    for y in range(nImgHeight):
        CountX = 0
        for x in range(nImgWidth):
            if imgCropImg.getpixel((x, y)) == 0:  # 黑色点
                CountX += 1
        PixelCountList.append(CountX)
    for x in range(nImgWidth):
        CountY = 0
        for y in range(nImgHeight):
            if imgCropImg.getpixel((x, y)) == 0:  # 黑色点
                CountY += 1
        PixelCountList.append(CountY)
    return PixelCountList

def OutPutVectorData(strID,strMaterialDir,strOutPath):
    for ParentPath,DirNames,FileNames in os.walk(strMaterialDir):
        with open(strOutPath, 'a') as fpFea:
            for fp in FileNames:
                strFullPath = os.path.join(ParentPath,fp) # 图片文件路径信息
                imgOriImg = Image.open(strFullPath)       # 打开图片
                FeatureList = GetFeature(imgOriImg,14,13) # 生成特征值
                strFeature = strID+' '
                nCount = 1
                for i in FeatureList:
                    strFeature = '%s%d:%d ' % (strFeature,nCount,i)
                    nCount+=1
                fpFea.write(strFeature+'\n')
                fpFea.flush()
        fpFea.close()

def TrainSvmModel(strProblemPath,strModelPath):
    Y, X = svm_read_problem(strProblemPath)
    Model = svm_train(Y,X)
    svm_save_model(strModelPath, Model)

def SvmModelTest(strProblemPath,strModelPath):
    TestY, TestX = svm_read_problem(strProblemPath)
    Model = svm_load_model(strModelPath)
    pLabel, pAcc, pVal = svm_predict(TestY, TestX, Model)#p_label即为识别的结果
    return pLabel

for i in range(0,10):
    strID = '%d' % i
    OutPutVectorData(strID,'D:/123/step_3/'+strID,'D:/123/step_4/Vector.txt')
for j in range(97,123):
    OutPutVectorData('%d'%j,'D:/123/step_3/'+chr(j),'D:/123/step_4/Vector.txt')

    TrainSvmModel('D:/123/step_4/Vector.txt','D:/123/step_5/Model.txt')

pLabel = SvmModelTest('D:/123/Base/Test/Vector.txt','D:/123/step_5/Model.txt')
for i in pLabel:
    print('%d ' % i)
