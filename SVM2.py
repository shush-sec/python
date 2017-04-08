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
strStep1Dir = 'C:/tencent/step_1/'
strStep2Dir = 'C:/tencent/test/'
for ParentPath,DirNames,FileNames in os.walk(strStep1Dir):
    for i in FileNames:
        strFullPath = os.path.join(ParentPath,i)  
        imgBinImg = BinaryzationImg(strFullPath)
        imgClrImg = ClearNoise(imgBinImg)
        ImgList = GetCropImgs(imgClrImg)
        for img in ImgList:
            strImgName = "%04d%04d.png" % (g_Count,random.randint(0,9999))
            strImgPath = os.path.join(strStep2Dir,strImgName)
            img.save(strImgPath)
            g_Count += 1

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

strMaterialDir = 'C:/tencent/step_3/'
strOutDir = 'C:/tencent/test/'
for ParentPath,DirNames,FileNames in os.walk(strMaterialDir):
        with open(strOutDir, 'w') as fpFea:
            for fp in FileNames:
                strFullPath = os.path.join(ParentPath,fp)  
                imgOriImg = Image.open(strFullPath)       
                FeatureList = GetFeature(imgOriImg,14,13)  
                strFeature = strID+' '
                nCount = 1
                for i in FeatureList:
                    strFeature = '%s%d:%d ' % (strFeature,nCount,i)
                    nCount+=1
                fpFea.write(strFeature+'\n')
                fpFea.flush()
        fpFea.close()
