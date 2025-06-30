import streamlit as st
import speech_recognition as sr
from fpdf import FPDF
import sounddevice as sd
from scipy.io.wavfile import write
def recording(outputfile, duration, samplerate=44100):
    st.warning(f"Recording for {duration} seconds...")
    data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    st.info("Recording completed.")
    write(outputfile, samplerate, data)
    st.write(f"Audio saved to {outputfile}")

def audiototext(inputfile):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(inputfile) as source:
            st.info("Understanding...")
            audiodata = recognizer.record(source)
            st.write("Converting audio to text...")
            text = recognizer.recognize_google(audiodata)
            return text
    except sr.UnknownValueError:
        return "Sorry, speech was not clear. Please retry."
    except sr.RequestError as e:
        return f"Could not request results from the speech recognition service; {e}"
    except Exception as ex:
        return f"An error occurred: {ex}"

def texttopdf(text, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(output_pdf)
    st.write(f"Summary PDF saved as: {output_pdf}")

# for streamlit 
def main():
    st.title("Speech to Text and PDF Converter")
    duration = st.slider("Select recording duration (seconds)", min_value=5, max_value=200, value=30)
    recordedfile = "myaudio.wav"
    pdffile = "summary.pdf"
    if st.button("Start Recording"):
        recording(recordedfile, duration)

        # Convert audio to text
        writtentext = audiototext(recordedfile)
        st.write("Transcribed text:")
        st.write(writtentext)
        texttopdf(writtentext, pdffile)
        with open(pdffile, "rb") as pdf_file:
            st.download_button(label="Download PDF", data=pdf_file, file_name=pdffile, mime="application/pdf")
if __name__ == "__main__":
    main()
