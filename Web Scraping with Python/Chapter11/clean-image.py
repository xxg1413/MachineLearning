'''
利用 Pillow 库,我们可以创建一个 阈值过滤器来去掉渐变的背景色,只把文字留下来,从而让图片更加清晰
'''

from PIL import Image
import subprocess

def cleanFile(filePath, newFilePath):
    image = Image.open(filePath)

    #Set a threshold value for the image, and save
    image = image.point(lambda x: 0 if x<143 else 255)
    image.save(newFilePath)


    #子进程调用tesseract  Tesseract 最大的缺点是对渐变背景色的处理
    subprocess.call(["tesseract", newFilePath, "test"])
    
    #Open and read the resulting data file
    outputFile = open("test.txt", 'r')
    print(outputFile.read())
    outputFile.close()

cleanFile("text.png", "text_clean.png")