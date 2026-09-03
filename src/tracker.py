import time

class PhoneTracker:
    def __init__(self, time_threshold=5.0):
        self.time_threshold = time_threshold
        self.active_tracks = {}  
        self.alerted_tracks = set() 

    def update(self, current_detections):
        current_time = time.time()
        alerts = []
        current_ids = []

        for track_id, conf in current_detections:
            current_ids.append(track_id)
            
            if track_id not in self.active_tracks:
                self.active_tracks[track_id] = current_time
            else:
                duration = current_time - self.active_tracks[track_id]
                
                if duration >= self.time_threshold and track_id not in self.alerted_tracks:
                    alerts.append((track_id, duration, conf))
                    self.alerted_tracks.add(track_id)

        lost_tracks = set(self.active_tracks.keys()) - set(current_ids)
        for track_id in lost_tracks:
            del self.active_tracks[track_id]
            if track_id in self.alerted_tracks:
                self.alerted_tracks.remove(track_id)

        return alerts
