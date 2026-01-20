from ultralytics import YOLO
import os, csv

model = YOLO("yolov8n.pt")
IMAGE_DIR = "data/raw/images"
OUTPUT = "data/yolo_results.csv"

rows = []

for channel in os.listdir(IMAGE_DIR):
    for img in os.listdir(f"{IMAGE_DIR}/{channel}"):
        path = f"{IMAGE_DIR}/{channel}/{img}"
        result = model(path)[0]
        labels = [model.names[int(c)] for c in result.boxes.cls]
        rows.append([img.replace(".jpg",""), channel, ",".join(labels)])

with open(OUTPUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["message_id","channel","objects"])
    writer.writerows(rows)
