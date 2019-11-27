from flask import Flask, render_template, send_from_directory, Response, render_template, request
from camera import Camera, GuardarImagen, GuardarImagen1
#from Redneuronal import eval_face, add_face
import argparse
import forms

camera = Camera()
camera.Run()

app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r

@app.route("/")
def stream_page():
    return render_template("index.html")

@app.route('/Aprendizaje.html', methods = ['GET', 'POST'])
def Aprendizaje():
    comment_form = forms.CommentForm1(request.form)
    if request.method =='POST':
        im = camera.get_frame(bytes=False)
        GuardarImagen(im, comment_form.Z.data)
        #Aca va la funcion
        #RN=add_face("img/" + comment_form.Z.data)
        #print(RN)
        #eva_face
    return render_template('Aprendizaje.html', form=comment_form)

@app.route("/Identificador.html")
def Id():
    print("Hola----")
    return render_template("Identificador.html")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: img/png\r\n\r\n' + frame + b'\r\n')

@app.route("/captura")
def capture():
    im = camera.get_frame(bytes=False)
    GuardarImagen1(im,"qwerty")
    #EF=eval_face("img1/qwerty")
    #print(EF)
    return render_template("send_to_init.html")

@app.route("/Video")
def Video():
    return Response(gen(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port',type=int,default=5000, help="Running port")
    parser.add_argument("-H","--host",type=str,default='127.0.0.1', help="Address to broadcast")
    args = parser.parse_args()
    app.run(host=args.host,port=args.port)


#f = open("Registro.csv", a)
#f.write(comment_form.Z.data + "\n")
#f.close()

#Identificador.html
       