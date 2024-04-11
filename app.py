import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import detection as d
import location as l

# Define the Streamlit app
def app():
    st.title('Protected Environment Using Object Detection')

    # Sidebar with options for image, webcam, or video
    option = st.sidebar.selectbox('Choose Input Type:', ('Image','Webcam','Video'))
    st.text("Choose an option and provide an image or video/webcam to see results with Warnings and Alerts.")

    # Allow the user to provide an image or choose webcam/video based on the selected option

    if(st.sidebar.button("GET HELP")):
        # Call the get_current_location() function from loc.py
        l.get_current_location()
        st.stop()

    elif option == 'Image':
        image_input = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])
        if image_input is not None:
            img = cv2.imdecode(np.frombuffer(image_input.read(), np.uint8), 1)
            st.image(image_input, caption='Input Image', use_column_width=True)

            # Display warnings and draw bounding boxes
            detected_img = d.display_warning_and_boxes(img.copy(), st.empty())
            st.image(detected_img, caption='Detected Image', channels='BGR',use_column_width=True)
            # L.get_current_location()
            

    elif option == 'Webcam':
        stframe=st.empty()
        st.sidebar.markdown("---")

        stframe = st.empty()

        run = st.sidebar.button("Start")
        stop = st.sidebar.button("Stop")
        st.sidebar.markdown("---")

        if(run):
            cap = cv2.VideoCapture(0)
            st.subheader("Webcam is running.....")
            st.subheader("Detected Frame")
            while True:
                _, frame = cap.read()
                height, width, _ = frame.shape

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                # Display warnings and draw bounding boxes
                detected_frame = d.display_warning_and_boxes(frame.copy(), st.empty())
                st.image(detected_frame,channels='BGR', caption=timestamp)

                stframe.image(detected_frame,caption=timestamp,channels='BGR')
                # time.sleep(0.1)  # Adjust the delay as needed for smooth rendering
        else:
            st.subheader("Webcam is not running.....")


    elif option == 'Video':
        video_input = st.file_uploader('Choose a video', type=['mp4'])
        if video_input is not None:
            with open("uploaded_video.mp4", "wb") as f:
                f.write(video_input.read())

            st.video("uploaded_video.mp4")
            st.subheader("Output Video")

            # Process video frames and save the output video
            d.process_video_and_save("uploaded_video.mp4", "outpt_video.mp4")

            # Display a message indicating that the output video has been saved
            st.text("the Output video is saved as output_video.mp4" )


# Run the app
if __name__ == '__main__':
    app()