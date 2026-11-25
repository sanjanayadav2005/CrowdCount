import cv2
import numpy as np
class Heatmap:
    def __init__(self): self.accumulator=None
    def accumulate(self,frame,points):
        if self.accumulator is None or self.accumulator.shape[:2]!=frame.shape[:2]:
            self.accumulator=np.zeros(frame.shape[:2],dtype=np.float32)
        for x,y in points:
            cv2.circle(self.accumulator,(int(x),int(y)),18,1.0,-1)
        blurred=cv2.GaussianBlur(self.accumulator,(31,31),0)
        if blurred.max()>0: blended=cv2.applyColorMap(cv2.normalize(blurred,None,0,255,cv2.NORM_MINMAX).astype(np.uint8),cv2.COLORMAP_JET)
        else: blended=np.zeros_like(frame)
        return cv2.addWeighted(frame,.55,blended,.45,0)
