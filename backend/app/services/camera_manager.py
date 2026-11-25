import cv2, threading, time, base64
import numpy as np
from collections import deque
from ..vision.detector import PersonDetector
from ..vision.tracker import CentroidTracker
from ..vision.counter import box_in_zone
from ..vision.heatmap import Heatmap
class CameraManager:
    def __init__(self):
        self.workers={}; self.frames={}; self.stats={}; self.lock=threading.Lock()
    def start(self,camera_id,source,source_type="webcam",zones=None,confidence=.45):
        self.stop(camera_id)
        worker=threading.Thread(target=self._run,args=(camera_id,source,source_type,zones or [],confidence),daemon=True)
        worker.start(); self.workers[camera_id]={"thread":worker,"running":True}
        return True
    def stop(self,camera_id):
        if camera_id in self.workers: self.workers[camera_id]["running"]=False
    def get_frame(self,camera_id):
        with self.lock: return self.frames.get(camera_id)
    def get_stats(self,camera_id):
        with self.lock: return dict(self.stats.get(camera_id,{"total":0,"zones":{},"entries":0,"exits":0}))
    def _run(self,camera_id,source,source_type,zones,confidence):
        src=int(source) if source_type=="webcam" and str(source).isdigit() else source
        cap=cv2.VideoCapture(src)
        detector=PersonDetector(confidence=confidence); tracker=CentroidTracker(); heatmap=Heatmap(); seen=set(); entries=0
        last_seen={}
        while self.workers.get(camera_id,{}).get("running"):
            ok,frame=cap.read()
            if not ok:
                if source_type=="video": cap.set(cv2.CAP_PROP_POS_FRAMES,0)
                else: time.sleep(.5); continue
            detections=detector.detect(frame)
            tracks=tracker.update(detections)
            boxes=[]
            for box in detections:
                x,y,w,h,conf,_=box
                cx,cy=int(x+w/2),int(y+h/2)
                tid=next((tid for tid,p in tracks.items() if abs(p[0]-cx)<w*.55 and abs(p[1]-cy)<h*.55),None)
                if tid is not None:
                    last_seen[tid]=(cx,cy)
                    if tid not in seen:
                        seen.add(tid); entries+=1
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,220,255),2)
                    cv2.putText(frame,f"ID {tid} {conf:.2f}",(x,y-8),cv2.FONT_HERSHEY_SIMPLEX,.48,(0,220,255),2)
                    boxes.append((x,y,w,h))
            zone_counts={}
            for zone in zones:
                polygon=zone["coordinates"]
                pts=[(int(p[0]),int(p[1])) for p in polygon]
                if len(pts)>=3:
                    cv2.polylines(frame,[np.array(pts,np.int32)],True,(100,210,255),2)
                count=sum(1 for box in boxes if box_in_zone(box,pts))
                zone_counts[str(zone["id"])]={"name":zone["name"],"count":count}
            heatmap_frame=heatmap.accumulate(frame,list(tracks.values()))
            ok,jpg=cv2.imencode(".jpg",heatmap_frame,[cv2.IMWRITE_JPEG_QUALITY,75])
            if ok:
                with self.lock:
                    self.frames[camera_id]=base64.b64encode(jpg.tobytes()).decode("ascii")
                    self.stats[camera_id]={"total":len(tracks),"zones":zone_counts,"entries":entries,"exits":0}
            time.sleep(.08)
        cap.release(); self.frames.pop(camera_id,None)
camera_manager=CameraManager()
