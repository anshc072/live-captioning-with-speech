import streamlit as st
import speech_recognition as sr
import pyttsx3

# Creating class for speech recognition and text-to-speech
recognizer = sr.Recognizer()
user = "SIDD : "
engine = pyttsx3.init()

# Function to process audio and convert it to text
def captioning():
    with sr.Microphone() as source:
        st.write("Please start speaking...")
        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                st.write(user + text)  # Display the recognized text
                engine.say(text)  # Convert the text to speech
                engine.runAndWait()
            except sr.UnknownValueError:
                st.write("Sorry, I didn't understand that.")
                continue
st.title("live captioning ")
st.write("Click the button to start listening to your voice.")

button = st.button("Start Listening")

if button:
    captioning()

