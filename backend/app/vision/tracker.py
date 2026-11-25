from collections import OrderedDict
import math
class CentroidTracker:
    def __init__(self,max_disappeared=30,max_distance=90):
        self.next_id=1; self.objects={}; self.disappeared={}; self.max_disappeared=max_disappeared; self.max_distance=max_distance
    def update(self,boxes):
        if not boxes:
            gone=[]
            for object_id in list(self.disappeared):
                self.disappeared[object_id]+=1
                if self.disappeared[object_id]>self.max_disappeared: gone.append(object_id)
            for object_id in gone: self.objects.pop(object_id,None); self.disappeared.pop(object_id,None)
            return self.objects.copy()
        input_centroids=[(int(x+w/2),int(y+h/2)) for x,y,w,h,*_ in boxes]
        if not self.objects:
            for c in input_centroids:
                self.objects[self.next_id]=c; self.disappeared[self.next_id]=0; self.next_id+=1
        else:
            object_ids=list(self.objects.keys()); object_centroids=list(self.objects.values())
            used_rows=set(); used_cols=set(); matches=[]
            for row,(ox,oy) in enumerate(object_centroids):
                for col,(cx,cy) in enumerate(input_centroids):
                    distance=math.hypot(ox-cx,oy-cy)
                    if distance<=self.max_distance:
                        matches.append((distance,row,col))
            for _,row,col in sorted(matches):
                if row in used_rows or col in used_cols: continue
                object_id=object_ids[row]; self.objects[object_id]=input_centroids[col]; self.disappeared[object_id]=0
                used_rows.add(row); used_cols.add(col)
            for col,c in enumerate(input_centroids):
                if col not in used_cols:
                    self.objects[self.next_id]=c; self.disappeared[self.next_id]=0; self.next_id+=1
            for row,object_id in enumerate(object_ids):
                if row not in used_rows:
                    self.disappeared[object_id]+=1
                    if self.disappeared[object_id]>self.max_disappeared:
                        self.objects.pop(object_id,None); self.disappeared.pop(object_id,None)
        return self.objects.copy()
