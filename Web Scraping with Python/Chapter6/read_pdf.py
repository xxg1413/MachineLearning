from urllib.request import  urlopen

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import  TextConverter
from pdfminer.layout import  LAParams

from io import  StringIO
from io import  open


def readPDF(pdfFile):
    mgr = PDFResourceManager()
    ret = StringIO()
    la = LAParams()

    device = TextConverter(mgr, ret, laparams=la)

    process_pdf(mgr, device, pdfFile)
    device.close()
    content = ret.getvalue()

    ret.close()

    return content


pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
out = readPDF(pdfFile)
print(out)
pdfFile.close()


