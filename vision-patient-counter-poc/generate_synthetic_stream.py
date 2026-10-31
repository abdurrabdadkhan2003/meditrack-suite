import os
import cv2
import numpy as np

def create_synthetic_video(output_path="data/synthetic_clinic.mp4", duration_sec=15, fps=30):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width, height = 800, 600
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames = duration_sec * fps
    print(f"Generating synthetic clinical test video at {output_path}...")

    for f in range(total_frames):
        # Blank clinic floor background
        frame = np.full((height, width, 3), 240, dtype=np.uint8)

        # Draw static clinic waiting chairs for visual context
        for cx in range(200, 650, 120):
            cv2.rectangle(frame, (cx, 380), (cx + 60, 430), (180, 180, 180), -1)

        cv2.putText(frame, "SYNTHETIC CLINIC FEED - COMPLIANCE SAFE", (20, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 2)

        out.write(frame)

    out.release()
    print("Synthetic video generation complete.")

if __name__ == "__main__":
    create_synthetic_video()
