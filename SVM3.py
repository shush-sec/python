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
    OutPutVectorData(strID,'C:/tencent/step_3/'+strID,'C:/tencent/step_4/Vector.txt')
for j in range(97,123):
    OutPutVectorData('%d'%j,'C:/tencent/step_3/'+chr(j),'C:/tencent/step_4/Vector.txt')
