from app.vision.counter import point_in_zone, box_in_zone

def test_point_inside_polygon():
    polygon=[[0,0],[10,0],[10,10],[0,10]]
    assert point_in_zone((5,5),polygon)
    assert not point_in_zone((11,5),polygon)

def test_box_zone_overlap():
    polygon=[[0,0],[100,0],[100,100],[0,100]]
    assert box_in_zone((40,40,20,20),polygon)
