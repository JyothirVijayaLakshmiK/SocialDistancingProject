from flask import Flask, render_template, request,Response
from frame import func,initial
import cv2
import time
app = Flask(__name__)
option=''
f=''
@app.route('/')
def home():
	return render_template('index.html')
@app.route('/option',methods=['POST','GET'])
def get_option():
	global option
	option = request.form['options']
	if(option=='image'):
		return render_template('image.html')
	elif(option=='video'):
		return render_template('video.html')
	else:
		return render_template('index.html')
@app.route('/uploadimage', methods=['POST', 'GET'])
def get_input_image():
	if request.method == 'POST':
		global f
		f = request.files['image'].filename
		return render_template('finalresult.html')
	else:
		return render_template('index.html')

@app.route('/uploadvideo', methods=['POST', 'GET'])
def get_input_video():
	if request.method == 'POST':
		global f
		f = request.files['video'].filename
		initial()
		cap=cv2.VideoCapture(f)
		ret,img = cap.read()
		fourcc = cv2.VideoWriter_fourcc(*'DIVX')
		writer = cv2.VideoWriter("output.avi",fourcc , 25,(img.shape[1], img.shape[0]), True)
		while(cap.isOpened):
			if ret == True:
				img=func(img)
				if writer is not None:
					writer.write(img)
			else:
				break
			ret,img = cap.read()
		cap.release()
		cv2.destroyAllWindows()
		writer.release()
		cv2.waitKey(1)
		return render_template('finalresult.html',option=option)
	else:
		return render_template('index.html')


def gen():
	if option=='image':		
		initial()
		file = cv2.imread(f)
		img=func(file)
		img=cv2.resize(img,(0,0),fx=1.0,fy=1.0)
		frame=cv2.imencode('.jpg',img)[1].tobytes()
		yield(b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n'+frame+b'\r\n')

	else:
		cap=cv2.VideoCapture("output.avi")
		while(cap.isOpened):
			ret,img = cap.read()
			if ret == True:
				img=cv2.resize(img,(0,0),fx=0.5,fy=0.5)
				frame=cv2.imencode('.jpg',img)[1].tobytes()
				yield(b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n'+frame+b'\r\n')
			else:
				break

@app.route('/imagevideo_feed')
def imagevideo_feed():
	return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
 	app.run(debug=True, port=5000) 