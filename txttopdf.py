import speech_recognition as sr
from fpdf import FPDF
import sounddevice as sd
from scipy.io.wavfile import write
import os 
from langchain import HuggingFaceHub

from langchain_community.llms import HuggingFaceHub
from fpdf import FPDF
from langchain import PromptTemplate
from langchain import LLMChain
# duration=input("Enter the duration for audio ")
#  recored audio from mic of the system 
huggingface_api_token=os.getenv("HUGGINGFACEHU_API_TOKEN")

def record_audio(outputfile, duration, samplerate=44100):

    print(f"Recording for {duration} seconds...")

    # Recording  audio
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("YOur recording is completed ")

    # Save the recorded audio to a WAV file
    write(outputfile, samplerate, audio_data)
    print(f"your audio is saved  saved to {outputfile}")

# duration=input("Enter the duration for audio ")
# record_audio("myaudio.wav" ,10, 44100)

def audiototext(input):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(input) as source:
            # Listening to the audio...
            audiodata = recognizer.record(source)

            print("Converting audio to text...")
            text = recognizer.recognize_google(audiodata)
            return text
    except sr.UnknownValueError:
        return "Sorry, speech was unclear."
    except sr.RequestError as e:
        return f"Could not request results from the speech recognition service; {e}"
    except Exception as ex:
        return f"An error occurred: {ex}"

def text_to_pdf(text, pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adding text to PDF
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)

    pdf.output(pdf)
    print(f"PDF saved as: {pdf}")

# Input audio file
inputfile = "cleannoise.wav"  
record_audio("myaudio.wav" ,10, 44100)
# Convert WAV to text
outputtext = audiototext(inputfile)
print("Transcribed Text:")
print(outputtext)

# Save the text as a PDF
pfilename = "summary.pdf"
text_to_pdf(outputtext, pfilename)