# import the necessary packages
import numpy as np
import cv2
import math
import os

def func(img):

    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    d1=[]
    centroids=[]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - (w / 2))
                y = int(center_y - (h / 2))
                # Rectangle coordinates

                boxes.append([x,y, w, h])
                centroids.append([center_x,center_y])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    count_ppl=0
    lf=[]
    c=[]
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if label=='person':
                cv2.circle(img, (centroids[i][0],centroids[i][1]), 5, (0,255,0), thickness=2, lineType=1, shift=0) 
                cv2.rectangle(img, (x,y), (x + w, y + h), (0,255,0), 2)
                lf.append([x,y,w,h])
                c.append(centroids[i])
                count_ppl+=1

    for i in range(len(lf)):
        for j in range(i+1,len(lf)):
            d=math.sqrt((c[j][1]-c[i][1])**2+(c[j][0]-c[i][0])**2)
            if d<72:
                cv2.circle(img, (c[i][0],c[i][1]), 5, (0,0,255), thickness=2, lineType=1, shift=0)
                cv2.circle(img, (c[j][0],c[j][1]), 5, (0,0,255), thickness=2, lineType=1, shift=0) 
                cv2.rectangle(img, (lf[i][0] ,lf[i][1] ), (lf[i][0]+lf[i][2] , lf[i][1]+lf[i][3]), (0,0,255), 2)
                cv2.rectangle(img, (lf[j][0] ,lf[j][1]), (lf[j][0]+lf[j][2] , lf[j][1]+lf[j][3] ), (0,0,255), 2)
                cv2.line(img, (c[i][0],c[i][1]),(c[j][0],c[j][1]), (0,0,255), 2)
                if j not in d1:
                    d1.append(j)
                if i not in d1:
                    d1.append(i)

    if len(d1)>10:
        a="    HIGH ALERT    "
        cv2.putText(img, a, (10, img.shape[0] - 50) , cv2.FONT_HERSHEY_DUPLEX , 1, (0,0,255), 2, cv2.LINE_AA)
        a=str(len(d1))+"people violates social distance!"
        cv2.putText(img, a, (10, img.shape[0] - 25) , cv2.FONT_HERSHEY_DUPLEX , 1, (0,0,255), 2, cv2.LINE_AA)
    elif count_ppl>=41:
        a="    HIGH ALERT    "
        cv2.putText(img, a, (10, img.shape[0] - 50) , cv2.FONT_HERSHEY_DUPLEX , 1, (0,0,255), 2, cv2.LINE_AA)
        a=str(count_ppl)+"people in your area!"
        cv2.putText(img, a, (10, img.shape[0] - 25) , cv2.FONT_HERSHEY_DUPLEX , 1, (0,0,255), 2, cv2.LINE_AA)

    else:  
        text="Total people Count : "+str(count_ppl)
        cv2.putText(img, text, (10, img.shape[0] - 50) , cv2.FONT_HERSHEY_DUPLEX , 1, (0,0,255), 2, cv2.LINE_AA)
        text="social Distance Violations : "+str(len(d1))   
        cv2.putText(img, text, (10, img.shape[0] - 25) , cv2.FONT_HERSHEY_DUPLEX , 1, (0,0,255), 2, cv2.LINE_AA)
                   
    return img
def initial():
    # Load Yolo
    global net,classes,layer_names,output_layers
    net = cv2.dnn.readNet("models/yolov3.weights", "models/yolov3.cfg")

    with open("models/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
   
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

