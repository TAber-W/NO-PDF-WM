
import sys
import os
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import QtCore,QtGui,QtWidgets,uic,Qt
from PyQt5.QtWidgets import QApplication,QFileDialog,QInputDialog,QDialog,QMessageBox
from PIL import Image
from itertools import product
import webbrowser
import fitz
import os


#import py
#from regex import W

sec=0
page_no = 0
col = 0
val = 0
filename = ""
disname = ""
class WorkThread(QThread):
    timer = pyqtSignal()
    end = pyqtSignal()
    def run(self):
        #打开源pfd文件
        pdf_file = fitz.open(filename[0])


        #page_no 设置为0
        global page_no
        #page在pdf文件中遍历
        for page in pdf_file:
            #self.sleep(1)
            self.timer.emit()
           
            #print(filename[0])
            trans = fitz.Matrix(int(col),int(col)).prerotate(0)
            #获取每一页对应的图片pix (pix对象类似于我们上面看到的img对象，可以读取、修改它的 RGB)
            #page.get_pixmap() 这个操作是不可逆的，即能够实现从 PDF 到图片的转换，但修改图片 RGB 后无法应用到 PDF 上，只能输出为图片
            pix = page.get_pixmap(matrix=trans, alpha=False)

            #遍历图片中的宽和高，如果像素的rgb值总和大于510，就认为是水印，转换成255，255,255-->即白色
            for pos in product(range(pix.width), range(pix.height)):
                if sum(pix.pixel(pos[0], pos[1])) >= val:
                    pix.set_pixel(pos[0], pos[1], (255, 255, 255))
            #保存去掉水印的截图
            pix.pil_save( disname+f'/{page_no}.png', dpi=(267, 267))
            #打印结果
            #print(f'第 {page_no} 页去除完成')

            page_no += 1
            
        self.end.emit()
        
    

class Stats:
    def __init__(self):
        self.ui = uic.loadUi("/Users/apple/Desktop/dad/pdf_none.ui")
        self.ui.setWindowTitle("PDF 去水印")
        self.ui.choosebutton.clicked.connect(self.xfile)
        self.ui.valuebutton.clicked.connect(self.xvalue)
        self.ui.colorbutton.clicked.connect(self.xcolor)
        self.ui.savebutton.clicked.connect(self.xsave)

        

        self.ui.workThread = WorkThread()

        self.ui.actionbangzhu.triggered.connect(self.go_github)
        
        
        self.ui.workThread.end.connect(self.end)
        self.ui.workThread.timer.connect(self.timer)
        self.ui.donebutton.clicked.connect(self.xwork)
        #self.ui.stopbutton.clicked.connect(self.xstop)

    def timer(self):
        self.ui.textEdit.append(f'第 {page_no} 页去除完成')

    def end(self):
        self.ui.textEdit.append(f'去除完成！！')
    
    def stop(self):
        print
        
    def xwork(self):
        if(filename=="") :
            self.ui.textEdit.append('请选择文件！')
        elif  int(col)==0:
            self.ui.textEdit.append('请选择清晰度！')
        elif disname == "":
            self.ui.textEdit.append('请选择保存位置!')
        else:
            self.ui.workThread.start()

    def xsave(self):
        global disname
        disname=QFileDialog.getExistingDirectory(self.ui,"xuanze","/")
        self.ui.saveline.setText(disname)

    def xvalue(self):
        global val
        val,ok = QInputDialog.getInt(self.ui,"水印数值","请输入水印RGB总和",255,0,765,2)
        print(val)

    def xfile(self):
        global filename
        filename= QFileDialog.getOpenFileName(self.ui,'dd',os.getcwd(),"All Files(*);Pdf Files(*.pdf)")
        self.ui.lineEdit.setText(filename[0])

        print(filename[0])

    def xcolor(self):
        items = ["1","2","5"]
        global col
        col,ok = QInputDialog.getItem(self.ui,"清晰度：会影响速度","请选择清晰度",items,0,True)
        if col != "1":
            self.ui.textEdit.append('清晰度较大，速度较慢，耐心等待')
        
    def go_github(self):
        print("ddd")
        url='https://github.com/TAber-W/NO-PDF-WM'
        webbrowser.open(url)


    
        

if __name__ == "__main__":
    App = QApplication(sys.argv)
    
    stats = Stats()
    stats.ui.setWindowIcon(QtGui.QIcon("/Users/apple/Desktop/dad/1.ico"))
    stats.ui.show()
    sys.exit(App.exec_())