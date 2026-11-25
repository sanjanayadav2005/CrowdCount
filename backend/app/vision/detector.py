import cv2
import os
import threading

class PersonDetector:
    def __init__(self, model_path="yolov8n.pt", confidence=.45):
        self.confidence=confidence
        self.model=None
        self.lock=threading.Lock()
        try:
            from ultralytics import YOLO
            self.model=YOLO(model_path)
        except Exception as exc:
            print(f"YOLO unavailable; detector is disabled until model loads: {exc}")
    def detect(self, frame):
        if self.model is None:
            return []
        with self.lock:
            results=self.model.predict(frame,classes=[0],conf=self.confidence,verbose=False)[0]
        detections=[]
        for box in results.boxes:
            x1,y1,x2,y2=map(int,box.xyxy[0].tolist())
            detections.append((x1,y1,x2-x1,y2-y1,float(box.conf[0]),"person"))
        return detections
