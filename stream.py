import pickle
import streamlit as st
from PIL import Image 
import requests
from transformers import AutoProcessor, BlipForConditionalGeneration
import speech_recognition as sr
import pyttsx3




def load_pickle_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as f:
        while True:
            try:
                chunk = pickle.load(f)
                yield chunk
            except EOFError:
                break


vqa_model_chunks = load_pickle_chunks('vqamodel.sav', chunk_size=1000000)
vqa_processor_chunks = load_pickle_chunks('vqaprocessor.sav', chunk_size=1000000)

def speak(text):
    engine = pyttsx3.init('sapi5')
    engine.setProperty('volume',1.0) 
    engine.setProperty('rate', 180)  
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")  
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)
    st.info("Stopped listening.")  
    try:
        query = r.recognize_google(audio)
        st.success("You said: " + query)  
        return query
    except:
        st.error("Sorry, could not understand audio.")  
        return 'None'

def process(input, text):
    image = Image.open(requests.get(input, stream=True).raw)
    processor = next(vqa_processor_chunks)
    model = next(vqa_model_chunks)
    if text == "describe":
        processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        inputs = processor(images=image, return_tensors="pt")
        output = model.generate(**inputs)
        return processor.decode(output[0], skip_special_tokens=True)
    else:
        inputs = processor(images=image, text=text, return_tensors="pt")
        output = model.generate(**inputs)
        return processor.decode(output[0], skip_special_tokens=True)

# Main function
def main():
    st.title('Talk to Image')
    image_url = st.text_input('Enter image URL')
    if image_url:
        st.image(image_url, caption='Image', use_column_width=True)
        option = st.radio("Choose input option:", ("Type question", "Use audio input"))
        if option == "Type question":
            question = st.text_input('Ask me any question')
            if st.button('Show Answer'):
                answer = process(image_url, question)
                st.success(answer)
                speak(answer)
                st.button("Continue asking questions")
        elif option == "Use audio input":
            question = takeCommand()
            answer = process(image_url, question)
            st.success(answer)
            speak(answer)
            st.button("Continue asking questions")

if __name__ == '__main__':
    main()
