import speech_recognition as sr
import pyttsx3
# creating class 
recognizer = sr.Recognizer() 
user="SIDD : "
# to make the audio retionable 
engine = pyttsx3.init()
def captioning():
    with sr.Microphone() as source:
        print("Now you can start to say")
        while True:
            try:
                audio = recognizer.listen(source) 
                text = recognizer.recognize_google(audio)
                print(user + text)
                engine.runAndWait()
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that.")
                break

if __name__ == "__main__":
    # This line checks whether the Python script is being run as the main program. 
    # If the script is executed directly (rather than being imported as a module), 
    # the block of code under it will be executed.
    captioning()
