import cv2
import numpy as np
from ultralytics import YOLO
from scipy.spatial.distance import cdist

model = YOLO("yolov8n.pt")

COLLISION_DISTANCE = 50

def process_frame(frame):

    results = model(frame)

    centers = []

    for r in results:
        for box in r.boxes:

            if int(box.cls[0]) == 0:

                x1,y1,x2,y2 = map(int,box.xyxy[0])

                cx = (x1+x2)//2
                cy = (y1+y2)//2

                centers.append((cx,cy))

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

    heatmap = np.zeros((frame.shape[0],frame.shape[1]),dtype=np.float32)

    for c in centers:
        cv2.circle(heatmap,c,40,1,-1)

    heatmap = cv2.GaussianBlur(heatmap,(51,51),0)

    heatmap = cv2.normalize(heatmap,None,0,255,cv2.NORM_MINMAX)

    heatmap = cv2.applyColorMap(heatmap.astype(np.uint8),cv2.COLORMAP_JET)

    frame = cv2.addWeighted(frame,0.6,heatmap,0.4,0)

    if len(centers) > 1:

        dist = cdist(centers,centers)

        for i in range(len(centers)):
            for j in range(i+1,len(centers)):

                if dist[i][j] < COLLISION_DISTANCE:

                    x1,y1 = centers[i]
                    x2,y2 = centers[j]

                    cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)

                    cv2.putText(frame,
                    "Collision Risk",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0,0,255),
                    2)

    return frame, len(centers)
