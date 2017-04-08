import requests
def Downloads_PIC(strPath,strName):
    url = 'http://www.bjgjj.gov.cn/wsyw/servlet/PicCheckCode1'
    rReq = requests.get(url, stream=True)
    with open(strPath+strName+'.png', 'wb') as fpPIC:
        for byChunk in rReq.iter_content(chunk_size=1024):
            if byChunk:
                fpPIC.write(byChunk)
                fpPIC.flush()
        fpPIC.close()

for i in range(1,20+1):
    strFileName = "%03d" % i
    Downloads_PIC('C:/tencent/step_1/',strFileName)
