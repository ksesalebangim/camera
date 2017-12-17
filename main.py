from flask import Flask
import io
import base64
from PIL import Image
import time
import glob
import subprocess
dropboxInLocation = ""
dropboxOutLocation = ""
printerMac = ""
app = Flask(__name__,static_folder='public', static_url_path='/public')
def getCamImage():
    return Image.open("/home/ben/1.jpg")


#TODO:add page reload every 1 sec
@app.route('/')
@app.route('/index')
def getImg():
    image = getCamImage()
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format="PNG")
    # reset file pointer to start
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()
    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
    return '<img id="content_img" src="data:image/png;base64,'+base64_encoded_result_str+'" />'


@app.route('/processed')
def processed():
    images = glob.glob(dropboxOutLocation + '*.jpg')
    ret = []
    for x in images:
        ret.append(x.split("/")[-1])
    return str(ret)


@app.route('/print/<filename>')
def printFile(filename):
    subprocess.Popen("obexftp --nopath --noconn --uuid none --bluetooth 70:2C:1F:2B:7D:85 --channel 4 -p "+dropboxOutLocation+filename+" "+filename, stdout=subprocess.PIPE, shell=True).stdout.read()
    return "move back to start of loop"



@app.route('/process/<fileData>')
def processImage(fileData):
    if str(fileData).startswith("data:image/png;base64,"):
        fileData = str(fileData).split("data:image/png;base64,",1)[1]
        mtime = int(time.time())
        pfile = open(dropboxInLocation+mtime+".jpg","w")
        pfile.write(fileData)
        pfile.close()


app.run(host='0.0.0.0')