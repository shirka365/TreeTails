from ultralytics import YOLO
import cv2
from YOLO_model import analyze_ouput
# Load the YOLOv8 model
# model = YOLO("C:\\Users\\User\PycharmProjects\TreeTailsModel\YOLO_model\\tree_features\yolov8_training15\weights\\best.pt")  # Replace with your trained YOLOv8 model path
model = YOLO(r"C:\Users\shira\PycharmProjects\TreeTails\YOLO_model\tree_features\yolov8_training15\weights\best.pt")  # Replace with your trained YOLOv8 model path

import json

# Open and read the JSON file
with open('indicator.json', 'r', encoding="utf-8") as file:
    indicator = json.load(file)

def run_yolo_on_image(image_path):
    """
    Run YOLOv8 on a real image and return the parsed output.

    Args:
        image_path (str): Path to the input image.

    Returns:
        list: YOLO output in the form of detected objects.
    """
    # Load the image
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    # Perform object detection
    results = model(image_path)

    # Parse YOLO output
    yolo_output = []
    for result in results[0].boxes:
        box = result.xyxy[0].tolist()  # Bounding box [x_min, y_min, x_max, y_max]
        label = result.cls[0]  # Class ID
        confidence = result.conf[0]  # Confidence score

        # Map label ID to class name
        class_name = model.names[int(label)]  # Replace with your class names if necessary

        yolo_output.append({
            "label": class_name,
            "bbox": [box[0], box[1], box[2], box[3]],
            "confidence": confidence
        })

    return yolo_output, image_width, image_height


# Path to your input image
# image_path = r"C:\Users\User\Desktop\WhatsApp_Image_2025-01-30_at_13.50.19_da6dec74.jpg"
image_path = r"C:\Users\shira\Downloads\ציור נועה.jpg"
# Step 1: Run YOLO on the real image
yolo_output, image_width, image_height = run_yolo_on_image(image_path)

# Step 2: Parse YOLO output to extract features
features = analyze_ouput.parse_yolo_output(yolo_output, image_width, image_height, indicator)

# Step 3: Generate personality output
personality_output = analyze_ouput.generate_personality_output(features, image_width, image_height,indicator)

# Step 4: Display results
print("Personality Analysis:")
print(personality_output[0])
print(personality_output[1])

# from ultralytics import YOLO
# import cv2
# import matplotlib.pyplot as plt
#
# # Load the trained YOLOv8 model
# model = YOLO(r"C:\Users\shira\PycharmProjects\TreeTails\YOLO_model\tree_features\yolov8_training14\weights\best.pt")  # Update the path if needed
#
# # Path to the image you want to test
# image_path = r"C:\Users\shira\Downloads\photo_2025-02-01_19-18-16.jpg" # Replace with the actual image path
#
# # Perform inference
# results = model(image_path)
#
# # Extract predictions
# boxes = results[0].boxes.xyxy.numpy()  # Bounding box coordinates [x_min, y_min, x_max, y_max]
# scores = results[0].boxes.conf.numpy()  # Confidence scores
# labels = results[0].boxes.cls.numpy()  # Class labels (numeric)
#
# # Class names (adjust based on your dataset's `data.yaml`)
# class_names = ["root", "trunk", "canopy"]  # Replace with your class labels if different
#
# # Load the image using OpenCV
# image = cv2.imread(image_path)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
# # Draw bounding boxes on the image
# for i, box in enumerate(boxes):
#     x_min, y_min, x_max, y_max = box
#     label = int(labels[i])
#     score = scores[i]
#
#     # Draw the bounding box
#     cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 0, 0), 2)
#
#     # Add label and confidence score
#     text = f"{class_names[label]}: {score:.2f}"
#     cv2.putText(image, text, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#
# # Visualize the image with bounding boxes
# plt.figure(figsize=(10, 10))
# plt.imshow(image)
# plt.axis("off")
# plt.title("YOLOv8 Predictions")
# plt.show()
