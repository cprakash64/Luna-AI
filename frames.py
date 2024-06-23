import cv2
import os
import pytesseract
import uuid
import torch
import numpy as np
from yolov5 import YOLOv5

# Initialize YOLO model
model = YOLOv5("yolov5s.pt", device="cpu")  # Use 'cuda' if you have a GPU

def extract_and_save_frames(video_path, output_dir, frame_interval=1):
    """
    Extracts and saves frames from a video at specified intervals, reads text using OCR,
    and performs object detection.

    Parameters:
    - video_path: str, path to the input video file
    - output_dir: str, directory to save the extracted frames
    - frame_interval: int, interval in seconds to extract frames
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    # Get video frame rate
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    success, frame = cap.read()
    count = 0

    # Open text file to save detected objects
    objects_txt_path = os.path.join(output_dir, "detected_objects.txt")
    with open(objects_txt_path, "w") as f:
        while success:
            if count % (frame_rate * frame_interval) == 0:
                timestamp = count / frame_rate
                minutes = int(timestamp // 60)
                seconds = int(timestamp % 60)
                frame_filename = os.path.join(output_dir, f"frame_{minutes}m_{seconds}s.jpg")
                cv2.imwrite(frame_filename, frame)
                print(f"Saved frame at {minutes} minutes and {seconds} seconds as {frame_filename}")

                # Perform OCR on the saved frame
                ocr_text = pytesseract.image_to_string(frame)
                print(f"OCR text at {minutes} minutes and {seconds} seconds: {ocr_text}")

                # Perform object detection on the saved frame
                results = model.predict(frame)
                objects = results.pandas().xyxy[0]  # Extracting the detected objects as a dataframe

                for _, obj in objects.iterrows():
                    label = obj['name']
                    confidence = obj['confidence']
                    box = obj[['xmin', 'ymin', 'xmax', 'ymax']].astype(int)
                    color = (0, 255, 0)  # Green bounding box

                    # Draw bounding box on the frame
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
                    cv2.putText(frame, f'{label} {confidence:.2f}', (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                    # Save detected object and timestamp to text file
                    f.write(f"Timestamp: {minutes}m{seconds}s - Object: {label}, Confidence: {confidence:.2f}\n")
                
                detected_frame_filename = os.path.join(output_dir, f"detected_{minutes}m_{seconds}s.jpg")
                cv2.imwrite(detected_frame_filename, frame)
                print(f"Detected objects in frame at {minutes} minutes and {seconds} seconds saved as {detected_frame_filename}")

            success, frame = cap.read()
            count += 1

    cap.release()
    print("Frame extraction and object detection completed.")

# Example usage
video_path = "/Users/chotu/Documents/MY_AI/Motivation Quickie - This Speech Will Pump You Up in 30 Seconds.mp4"  # Replace with your video file path
output_dir = "/Users/chotu/Documents/MY_AI/extracted_frames"  # Replace with your desired output directory
extract_and_save_frames(video_path, output_dir, frame_interval=1)
