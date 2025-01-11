from flask import Flask,request, render_template, Response
from flask_cors import CORS
import requests, json
import cv2
import time
# from onvif import ONVIFCamera
# import zeep

app = Flask(__name__)
CORS(app)


  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames(USER,PASSWORD,IP):  # generate frame by frame from camera
    camera = cv2.VideoCapture('rtsp://'+USER+':'+PASSWORD+'@'+IP+':554/cam/realmonitor?channel=1&subtype=1')

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        #frame_detection(frame)
	#if not success:
        #    break
        #else:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def hd_frames(USER,PASSWORD,IP):
    camera = cv2.VideoCapture('rtsp://'+USER+':'+PASSWORD+'@'+IP+':554')
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_image(USER,PASSWORD,IP):  # generate frame by frame from camera
    camera = cv2.VideoCapture('rtsp://'+USER+':'+PASSWORD+'@'+IP+':554')

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            break

XMAX = 0.3
XMIN = -0.3
YMAX = 0.3
YMIN = -0.3






@app.route('/video_feed',methods=['GET', 'POST'])
def video_feed():
    user = request.args.get('user')
    password = request.args.get('password')
    ip = request.args.get('ip')
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(user,password,ip), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_hd',methods=['GET', 'POST'])
def video_hd():
    user = request.args.get('user')
    password = request.args.get('password')
    ip = request.args.get('ip')
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(hd_frames(user,password,ip), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image_feed',methods=['GET', 'POST'])
def image_feed():
    user = request.args.get('user')
    password = request.args.get('password')
    ip = request.args.get('ip')
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_image(user,password,ip), mimetype='multipart/x-mixed-replace; boundary=frame')


    


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,host='192.168.213.217',port='5000', ssl_context=('cert.pem', 'priv_key.pem'))
