import os
import cv2
from ultralytics import YOLO
from zone_analytics import ClinicZoneAnalytics

def run_vision_pipeline():
    print("--- Checklife Vision PoC: ROI & Dwell Time Engine ---")
    model = YOLO("yolov8n.pt")

    video_path = "data/synthetic_clinic.mp4"
    if not os.path.exists(video_path):
        print("[INFO] Using live webcam feed (Press 'q' to exit)...")
        cap = cv2.VideoCapture(0)
    else:
        print(f"[INFO] Reading video stream: {video_path}")
        cap = cv2.VideoCapture(video_path)

    # Read first frame to dynamically scale ROI zones to your camera resolution
    success, first_frame = cap.read()
    if not success:
        print("[ERROR] Could not read video source.")
        return

    h, w, _ = first_frame.shape
    tripwire_y = int(h * 0.40)
    waiting_polygon = [
        (int(w * 0.15), int(h * 0.45)),
        (int(w * 0.85), int(h * 0.45)),
        (int(w * 0.90), int(h * 0.92)),
        (int(w * 0.10), int(h * 0.92))
    ]

    analytics = ClinicZoneAnalytics(line_y=tripwire_y, waiting_zone_polygon=waiting_polygon)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Track people (class 0) across frames
        results = model.track(frame, persist=True, classes=[0], verbose=False)

        boxes = []
        track_ids = []

        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()

        # Update tripwire counts and waiting room dwell times
        analytics.process_detections(boxes, track_ids)

        # Render visual HUD and zone overlays
        annotated_frame = analytics.draw_overlays(frame, boxes, track_ids)

        cv2.imshow("Meditrack ROI & Wait-Time Engine", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Final Session Metrics:", analytics.get_metrics())

if __name__ == "__main__":
    run_vision_pipeline()
