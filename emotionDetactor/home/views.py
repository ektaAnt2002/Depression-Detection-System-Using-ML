# views.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.shortcuts import render, redirect
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from django.conf import settings
from django.core.mail import send_mail
from default.models import Profile
from django.contrib.auth.models import User
from .models import Appointments
from django.http import HttpResponseRedirect
from django.contrib import messages
import nltk
nltk.download('vader_lexicon')


def detect_emotion(request):
    emotion_model = load_model(r'C:\Users\ektaa\Downloads\send_ekta\emotionDetactor\detection_model\facialemotionmodel.h5')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  
    cap = cv2.VideoCapture(0)

    detected_emotion = "Sad"
    while True:
        try:
            ret, frame = cap.read()
            print(frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face_roi = gray[y:y + h, x:x + w]

                face_roi = cv2.resize(face_roi, (48, 48))

                face_roi = face_roi / 255.0

                face_roi = np.reshape(face_roi, (1, 48, 48, 1))

                emotion_prediction = emotion_model.predict(face_roi)

                emotion_label = np.argmax(emotion_prediction)

                emotion_labels = {0: 'Angry', 1: 'Disgust', 2: 'Fear',
                                  3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

                detected_emotion = emotion_labels[emotion_label]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, detected_emotion, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        except:
            pass

        if frame.shape[0] > 0 and frame.shape[1] > 0:
            cv2.imshow('Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    doctor_list = Profile.objects.filter(
        registeras="1")
    messages.warning(request, "Detected Emotion : " + detected_emotion)
    return render(request, 'doctors.html', {
        'doctor_list': doctor_list
    })


def analyze_sentiment(request):

    return render(request, 'index.html')


def home(request):

    doctor_list = Profile.objects.filter(registeras="1")[:4]
    doctor_list_name = Profile.objects.filter(registeras="1")
    return render(request, 'index.html', {
        "doctor_list": doctor_list,
        "doctor_list_name": doctor_list_name

    })


def about(request):
    return render(request, 'about.html')


def doctors(request):
    doctor_list = Profile.objects.filter(registeras="1")
    return render(request, 'doctors.html', {
        "doctor_list": doctor_list

    })


def contact(request):
    return render(request, 'contact.html')


def sevices(request):
    return render(request, 'sevices.html')


def sentiments(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Perform sentiment analysis
        sentiment_analyzer = SentimentIntensityAnalyzer()
        print(sentiment_analyzer)
        sentiment_score = sentiment_analyzer.polarity_scores(user_input)[
            'compound']
        print(sentiment_score)

        # Map sentiment score to your defined classes
        if sentiment_score >= 0.05:
            sentiment_label = 'Happy'
        elif sentiment_score <= -0.05:
            sentiment_label = 'Sad'
        else:
            sentiment_label = 'Neutral'

        print(sentiment_label)
        if (sentiment_label == "Sad" or sentiment_label == "Neutral"):
            messages.warning(
                request, "Detected Sentiment : " + sentiment_label)
            return redirect('all_doctors')
    return render(request, 'sentiments.html')


def book_appointment(request, email):
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        email_patient = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        doctor_name = request.POST.get("doctor_name")
        date = request.POST.get("date")
        time = request.POST.get("time")
        description = request.POST.get("description")

        Appointments.objects.create(
            doctor=User.objects.get(username=doctor_name),
            patient=username,
            date=date,
            time=time,
            description=description,
            phone_number=phone_number
        )

        subject_patient = "Booked : Appointment Has been booked"
        subject_doctor = "You have new appointment."
        email_from = settings.EMAIL_HOST_USER
        zoom_meeting = settings.ZOOM_MEETING_LINK
        message_patient = f"Your appointment has been booked at {date} on {time}. Your meeting link : {zoom_meeting}"
        message_doctor = f"Please try to be available at {date} on {time}. Your meeting link : {zoom_meeting}"

        try:
            send_mail(subject_patient, message_patient,
                      email_from, [email_patient])
            send_mail(subject_doctor, message_doctor, email_from, [email])
        except Exception as e:
            print(e)
        messages.warning(request, "This Email is already used.")
        return HttpResponseRedirect('/home/login')
    return render(request, 'appointment.html', {"doctor_name": email})


def quiz(request):
    if request.method == "POST":
        messages.warning(
            request, "Detected Result : Sad")
        return redirect('all_doctors')
    return render(request, 'quiz.html')

