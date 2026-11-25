def point_in_zone(point,polygon):
    x,y=point
    inside=False
    if len(polygon)<3: return False
    j=len(polygon)-1
    for i in range(len(polygon)):
        xi,yi=polygon[i]; xj,yj=polygon[j]
        if ((yi>y)!=(yj>y)) and (x<(xj-xi)*(y-yi)/(yj-yi+1e-9)+xi): inside=not inside
        j=i
    return inside
def box_in_zone(box,polygon):
    x,y,w,h=box
    center=(int(x+w/2),int(y+h/2))
    return point_in_zone(center,polygon)
