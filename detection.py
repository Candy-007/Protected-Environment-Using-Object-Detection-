import streamlit as st
import cv2
import numpy as np
import time
import keys as k

# Load YOLO model for fire and weapon detection
combined_net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
combined_classes = [line.strip() for line in open('obj.names')]
conf_threshold = 0.6

# Function to detect objects in Images
def detect_objects(image):
    h, w, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    combined_net.setInput(blob)
    output_layer_names = combined_net.getUnconnectedOutLayersNames()
    detections = combined_net.forward(output_layer_names)

    boxes = []
    confidences = []
    class_ids = []

    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > conf_threshold:
                center_x = int(obj[0] * w)
                center_y = int(obj[1] * h)
                width = int(obj[2] * w)
                height = int(obj[3] * h)

                # Calculate bounding box coordinates
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                boxes.append([x, y, width, height])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids

# Function to process video frames and save the output video
def process_video_and_save(input_path, output_path):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = 2  # Process two frames per second 

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create VideoWriter object to save the processed frames
    out_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps/10, (width, height))

    frame_count = 0
    stframe=st.empty()

    st.subheader("Detected Frames")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process two frames per second
        if frame_count % int(fps / frame_interval) == 0:

            # Get current timestamp
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            # Display warnings and draw bounding boxes
            detected_frame = display_warning_and_boxes(frame.copy(), st.empty())

            st.image(detected_frame, caption=f'Timestamp: {timestamp:.2f}', channels='BGR', use_column_width=True)

            stframe.image(detected_frame,channels='BGR')
            time.sleep(0.1)  # Adjust the delay as needed for smooth rendering

            # Write the processed frame to the output video
            out_video.write(detected_frame)

        frame_count += 1

    cap.release()
    out_video.release()

# Function to display warnings and draw bounding boxes
def display_warning_and_boxes(image, warning_container):
    boxes, confidences, class_ids = detect_objects(image)

    # Clear previous warning message
    warning_container.empty()

    # Display warning messages
    pred_labels = [combined_classes[class_id] for class_id in class_ids]

    if 'Fire' in pred_labels and 'Gun' in pred_labels:

        warning_container.markdown(
            '<div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">'
            '<h2 style="color: #ff0000;">DOUBLE_WARNING: FIRE AND WEAPON DETECTED! UNSAFE ENVIRONMENT. PLEASE PROTECT YOURSELF!</h2>'
            '</div>',
            unsafe_allow_html=True
        )
        # time.sleep(2)  # Display the warning for 2 seconds
        # k.send_sms('Double')
        # k.beep()
        # k. speak_warning("Double Warning: Fire and weapon detected! Unsafe environment. Please protect yourself!")

    elif 'Fire' in pred_labels and 'Rifle' in pred_labels:

        warning_container.markdown(
            '<div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">'
            '<h2 style="color: #ff0000;">DOUBLE_WARNING: FIRE AND WEAPON DETECTED! UNSAFE ENVIRONMENT. PLEASE PROTECT YOURSELF!</h2>'
            '</div>',
            unsafe_allow_html=True
        )
        # time.sleep(2)  # Display the warning for 2 seconds
        # k.send_sms('Double')
        # # k.beep()
        # k. speak_warning("Double Warning: Fire and weapon detected! Unsafe environment. Please protect yourself!")
    elif 'Fire' in pred_labels:

        warning_container.markdown(
            '<div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">'
            '<h2 style="color: #ff0000;">WARNING: FIRE DETECTED! UNSAFE ENVIRONMENT. PLEASE PROTECT YOURSELF!</h2>'
            '</div>',
            unsafe_allow_html=True
        )
        # time.sleep(2)  # Display the warning for 2 seconds
        # k.send_sms('fire')
        k.beep()
        k. speak_warning("WARNING: FIRE DETECTED! UNSAFE ENVIRONMENT. PLEASE PROTECT YOURSELF!")
    elif 'Gun' in pred_labels or 'Rifle' in pred_labels:

        warning_container.markdown(
            '<div style="background-color: #ffcccc; padding: 10px; border-radius: 5px;">'
            '<h2 style="color: #ff0000;">WARNING: WEAPON DETECTED! UNSAFE ENVIRONMENT. PLEASE PROTECT YOURSELF!</h2>'
            '</div>',
            unsafe_allow_html=True
        )
        # time.sleep(2)  # Display the warning for 2 seconds
        # k.send_sms('weapon')
        # k.beep()
        # k. speak_warning("WARNING: WEAPON DETECTED! UNSAFE ENVIRONMENT. PLEASE PROTECT YOURSELF!")

    else:
        # Display the safe message with green background
        warning_container.markdown(
            '<div style="background-color: #ccffcc; padding: 10px; border-radius: 5px;">'
            '<h2 style="color: #008000;">YOU ARE IN A SAFE ENVIRONMENT</h2>'
            '</div>',
            unsafe_allow_html=True
        )

    # Draw bounding boxes on the image
    for i in range(len(boxes)):
        x, y, width, height = boxes[i]

        # Draw bounding box on the image
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Display class label and confidence
        label = f'{combined_classes[class_ids[i]]}: {confidences[i]:.2f}'
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0,255), 2)

    return image