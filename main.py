from flask import Flask, render_template, send_from_directory, Response
from camera import Camera, GuardarImagen
import argparse

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

@app.route("/captura")
def capture():
    im = camera.get_frame(bytes=False)
    GuardarImagen(im)
    return render_template("send_to_init.html")

@app.route("/img/last")
def last_image():
    Pathh = Path("img/last.png")
    if Pathh.exists():
        r = "last.png"
    else:
        print("No last")
        r = "not_found.jpeg"
    return send_from_directory("img",r)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: img/png\r\n\r\n' + frame + b'\r\n')


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
