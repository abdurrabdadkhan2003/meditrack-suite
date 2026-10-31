import time
import cv2
import numpy as np

class ClinicZoneAnalytics:
    def __init__(self, line_y: int, waiting_zone_polygon: list):
        self.line_y = line_y
        self.waiting_zone = np.array(waiting_zone_polygon, np.int32)

        # Tracking state
        self.previous_y = {}
        self.entered_ids = set()

        # Dwell time tracking: {track_id: first_seen_timestamp}
        self.zone_entry_times = {}
        # Current dwell duration in seconds: {track_id: duration_sec}
        self.current_dwell_times = {}
        self.active_zone_ids = set()

    def process_detections(self, boxes, track_ids):
        self.active_zone_ids.clear()
        current_time = time.time()

        for box, track_id in zip(boxes, track_ids):
            x1, y1, x2, y2 = map(int, box)
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            bottom_center = (cx, y2)

            # 1. Tripwire Line Crossing Check (Moving downwards across line_y)
            if track_id in self.previous_y:
                prev_cy = self.previous_y[track_id]
                if prev_cy < self.line_y and cy >= self.line_y:
                    self.entered_ids.add(track_id)
            self.previous_y[track_id] = cy

            # 2. Waiting Room Polygon ROI Check
            is_inside = cv2.pointPolygonTest(self.waiting_zone, bottom_center, False) >= 0
            if is_inside:
                self.active_zone_ids.add(track_id)
                if track_id not in self.zone_entry_times:
                    self.zone_entry_times[track_id] = current_time
                self.current_dwell_times[track_id] = current_time - self.zone_entry_times[track_id]
            else:
                # Reset timer if they leave the waiting zone
                self.zone_entry_times.pop(track_id, None)
                self.current_dwell_times.pop(track_id, None)

    def get_metrics(self):
        occupancy = len(self.active_zone_ids)
        if occupancy > 0:
            avg_wait = sum(self.current_dwell_times[tid] for tid in self.active_zone_ids) / occupancy
        else:
            avg_wait = 0.0

        return {
            "total_footfall": len(self.entered_ids),
            "current_occupancy": occupancy,
            "avg_wait_seconds": round(avg_wait, 1)
        }

    def draw_overlays(self, frame, boxes, track_ids):
        height, width, _ = frame.shape

        # Draw Entrance Tripwire
        cv2.line(frame, (0, self.line_y), (width, self.line_y), (0, 255, 255), 2)
        cv2.putText(frame, "ENTRANCE TRIPWIRE", (10, self.line_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Draw Semi-Transparent Waiting Room Zone
        overlay = frame.copy()
        cv2.fillPoly(overlay, [self.waiting_zone], (255, 100, 0))
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        cv2.polylines(frame, [self.waiting_zone], True, (255, 100, 0), 2)

        # Draw Bounding Boxes & Individual Dwell Timers
        for box, track_id in zip(boxes, track_ids):
            x1, y1, x2, y2 = map(int, box)
            in_zone = track_id in self.active_zone_ids
            color = (0, 255, 0) if in_zone else (200, 200, 200)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"ID #{track_id}"
            if in_zone:
                wait_sec = int(self.current_dwell_times.get(track_id, 0))
                label += f" | Wait: {wait_sec}s"

            cv2.putText(frame, label, (x1, max(20, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

        # Draw Top-Left Telemetry HUD
        metrics = self.get_metrics()
        cv2.rectangle(frame, (10, 10), (330, 115), (20, 20, 20), -1)
        cv2.putText(frame, f"Total Footfall: {metrics['total_footfall']}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        cv2.putText(frame, f"Waiting Occupancy: {metrics['current_occupancy']}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        cv2.putText(frame, f"Avg Wait Time: {metrics['avg_wait_seconds']}s", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 215, 255), 2)

        return frame
