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
huggingface_api_token=os.getenv("HUGGINGFACEHU_API_TOKEN")
# Text cleaning function
def clean_text(text):
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201C": '"',
        "\u201D": '"',
        "\u2013": "-",
        "\u2014": "-",
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

def recording(outputfile, duration, samplerate=44100):
    print(f"recording for {duration} seconds...")
    data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    # wait kro jb tgk recaurding finish nhi jo jati hai 
    sd.wait()
    print("your recording is completed .")
    write(outputfile, samplerate, data)
    print(f"audio saved to {outputfile}")
def audiototext(inputfile):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(inputfile) as source:
            print("understanding....")
            audiodata = recognizer.record(source)
            print("Converting audio to text...")
            text = recognizer.recognize_google(audiodata)
            return text
    except sr.UnknownValueError:
        return "Sorry, speech was not clear reTRY."
    except sr.RequestError as e:
        return f"Could not request results from the speech recognition service; {e}"
    except Exception as ex:
        return f"An error occurred: {ex}"
    
def predict(text):
    llm =HuggingFaceHub(repo_id="utrobinmv/t5_summary_en_ru_zh_base_2048", model_kwargs={"temperature":0,"max_length":64}  )
    prompt = PromptTemplate(input_variables=['text'], template='Summarizing the following text in English: {text}')
    chain = LLMChain(llm=llm, prompt=prompt)
    summary = chain.run(text)
    return summary

def texttopdf(text, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(output_pdf)
    print(f"PDF saved as: {output_pdf}")

def main():
    recordedaudiofile = "myaudio.wav"
    pdffile= "summary.pdf"
    duration = 30

    # 1111 recording 
    recording(recordedaudiofile, duration)

    # 2222  text write 
    writtentext = audiototext(recordedaudiofile)
    rittentext=clean_text(writtentext)

    newtext=predict(rittentext)
    # newtext=predict(transcribed_text )
    print("your text is {newtext}")
    # 3333
    texttopdf(newtext , pdffile)
main()
if __name__ == "_main_":
    main()
