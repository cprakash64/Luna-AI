import cv2
import torch
from ultralytics import YOLO
import os

class ObjectDetector:
    def __init__(self):
        self.model = YOLO("yolov5s.pt")  # Load pre-trained YOLOv5 model

    def extract_frames(self, video_path, interval=30):
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps

        frames = []
        timestamps = []
        success, frame = cap.read()
        count = 0

        while success:
            if count % interval == 0:
                frames.append(frame)
                timestamps.append(count / fps)
            success, frame = cap.read()
            count += 1

        cap.release()
        return frames, timestamps

    def detect_objects(self, frames, target_objects):
        detected_objects = []
        for i, frame in enumerate(frames):
            results = self.model(frame)
            for result in results.xyxy[0]:
                label = self.model.names[int(result[-1])]
                if label in target_objects:
                    detected_objects.append((i, label, frame))
        return detected_objects

    def find_object_in_video(self, video_path, target_objects):
        frames, timestamps = self.extract_frames(video_path)
        detected_objects = self.detect_objects(frames, target_objects)
        results = [(timestamps[i], label, frame) for i, label, frame in detected_objects]
        return results
