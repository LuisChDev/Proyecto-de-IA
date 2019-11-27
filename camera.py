import os
import cv2
import shutil
import threading
import time, datetime
from pathlib import Path

thread = None

class Camera:
    def __init__(self, fps = 20, FuenteDelVideo = 0):
        self.fps = fps
        self.FuenteDelVideo = FuenteDelVideo
        self.camera = cv2.VideoCapture(self.FuenteDelVideo)
        self.FMax = self.fps * 5
        self.frames = []
        self.run = False

    def Run(self):
        global thread
        if thread is None:
            thread = threading.Thread(target=self.Cap)
            print("Starting thread...")
            thread.start()
            self.run = True

    def Cap(self):
        dt = 1/self.fps
        print("Observing...")
        while self.run:
            boool,i = self.camera.read()
            if boool:
                if len(self.frames)==self.FMax:
                    self.frames = self.frames[1:]
                self.frames.append(i)
            time.sleep(dt)

    def stop(self):
        self.run = False

    def get_frame(self, bytes=True):
        if len(self.frames)>0:
            if bytes:
                Img = cv2.imencode('.png',self.frames[-1])[1].tobytes()
            else:
                Img = self.frames[-1]
        else:
            with open("img/not_found.jpeg","rb") as f:
                Img = f.read()
        return Img


def GuardarImagen(im, nomb):
    s = im.shape
    # Add a timestamp
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,s[0]-10)
    fontScale = 1
    fontColor = (20,20,20)
    lineType = 2

    cv2.putText(im,datetime.datetime.now().isoformat().split(".")[0],bottomLeftCornerOfText,font,fontScale,fontColor, lineType)

    Dirc = nomb + "/"
    #cop= "/img/" + nomb
    try:
        os.mkdir("img/" + nomb)
    except OSError:
        print ("holi")


    m = 0
    p = Path("img/" + nomb)
    for imp in p.iterdir():
        if imp.suffix == ".png" and imp.stem != "last":
            num = imp.stem.split("_")[1]
            try:
                num = int(num)
                if num>m:
                    m = num
            except:
                print("Error reading image number for",str(imp))
    m +=1
    
    #shutil.copy('/img/last.png', cop)  #Copiar y pegar ficheros
    lp = Path("img/"+ Dirc + "last.png")
    if lp.exists() or lp.is_file():
        np = Path("img/"+ Dirc +"img_{}.png".format(m))
        np.write_bytes(lp.read_bytes())
    cv2.imwrite("img/"+ Dirc +"last.png", im)


def GuardarImagen1(im, nomb):
    s = im.shape
    # Add a timestamp
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,s[0]-10)
    fontScale = 1
    fontColor = (20,20,20)
    lineType = 2

    cv2.putText(im,datetime.datetime.now().isoformat().split(".")[0],bottomLeftCornerOfText,font,fontScale,fontColor, lineType)

    Dirc = nomb + "/"
    #cop= "/img/" + nomb
    try:
        os.mkdir("img1/" + nomb)
    except OSError:
        print ("holi")


    m = 0
    p = Path("img1/" + nomb)
    for imp in p.iterdir():
        if imp.suffix == ".png" and imp.stem != "last":
            num = imp.stem.split("_")[1]
            try:
                num = int(num)
                if num>m:
                    m = num
            except:
                print("Error reading image number for",str(imp))
    m +=1
    
    #shutil.copy('/img/last.png', cop)  #Copiar y pegar ficheros
    lp = Path("img1/"+ Dirc + "last.png")
    if lp.exists() or lp.is_file():
        np = Path("img1/"+ Dirc +"img_{}.png".format(m))
        np.write_bytes(lp.read_bytes())
    cv2.imwrite("img1/"+ Dirc +"last.png", im)