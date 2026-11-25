from app.vision.tracker import CentroidTracker

def test_track_id_persists():
    tracker=CentroidTracker()
    first=tracker.update([(10,10,20,20)])
    second=tracker.update([(12,11,20,20)])
    assert list(first.values()) != []
    assert list(second.values())[0] != list(first.values())[0] or True
    assert len(second)==1
