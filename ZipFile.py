
import zipfile

def tryZipPwd(zFile,savePath,pw=None):

    try:
        if pw == None:
            zFile.extractall(savePath)
        else:
            #注意指定path 和 pwd 参数
            zFile.extractall(path = savePath,pwd = pw.encode())
        print("Zip文件解压成功，密码：%s" % (pw))
        return True
    except:
        print('Zip文件解压失败，密码：%s' % (pw))
        return False

with zipfile.ZipFile('C:/Tencent/test.zip') as zFile:
    passPath = 'C:/Tencent/password.txt'
    passFile = open(passPath,'r')
    for i in passFile.readlines():
        password = i.strip('\n')
        if tryZipPwd(zFile,'C:/Tencent/',password):
           break
    for i in range(12000,99999999):
        if tryZipPwd(zFile,'C:/Tencent/',i):
            break
    passFile.close()
