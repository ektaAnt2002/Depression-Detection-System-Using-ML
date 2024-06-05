from tensorflow.keras.models import load_model
import cv2
import numpy as np
from default.models import Profile
from django.contrib import messages
from django.shortcuts import render, redirect


def detect_emotion(request):
    # Load pre-trained emotion detection model (FER2013)
    # Provide the correct path
    emotion_model = load_model('model_v6_23.hdf5')

    # Load Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')  # Provide the correct path

    # Access webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        try:
            ret, frame = cap.read()
            print(frame)

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            # Iterate over detected faces
            for (x, y, w, h) in faces:
                # Crop the face from the frame
                face_roi = gray[y:y + h, x:x + w]

                # Resize the face image to fit the model input size
                face_roi = cv2.resize(face_roi, (48, 48))

                # Normalize pixel values
                face_roi = face_roi / 255.0

                # Reshape for model input
                face_roi = np.reshape(face_roi, (1, 48, 48, 1))

                # Predict emotion using the loaded model
                emotion_prediction = emotion_model.predict(face_roi)

                # Get the index with the highest probability as the predicted emotion
                emotion_label = np.argmax(emotion_prediction)

                # Define emotion labels (modify as needed)
                emotion_labels = {0: 'Angry', 1: 'Disgust', 2: 'Fear',
                                  3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

                # Get the corresponding emotion label
                detected_emotion = emotion_labels[emotion_label]
                # Draw a rectangle around the detected face and display the emotion label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, detected_emotion, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        except:
            pass

        # Display the resulting frame
        cv2.imshow('Emotion Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    doctor_list = Profile.objects.filter(
        registeras="1")
    messages.warning(request, "Detected Emotion : " + detected_emotion)
    return render(request, 'doctors.html', {
        'doctor_list': doctor_list
    })
