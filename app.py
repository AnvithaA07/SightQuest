from flask import Flask, render_template, request, jsonify
import pickle
import requests
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration


def load_pickle_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as f:
        while True:
            try:
                chunk = pickle.load(f)
                yield chunk
            except EOFError:
                break

# Load VQA model and processor in chunks
vqa_model_chunks = load_pickle_chunks('vqamodel.sav', chunk_size=1000000)
vqa_processor_chunks = load_pickle_chunks('vqaprocessor.sav', chunk_size=1000000)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    img = request.files['fileUpload']
    option = request.form['option']
    img_name = img.filename
    image = Image.open(img)

    if option=='talk':
        text="What is that?"
        processor = next(vqa_processor_chunks)
        model = next(vqa_model_chunks)
        inputs = processor(images=image, text=text, return_tensors="pt")
        output = model.generate(**inputs)
        return processor.decode(output[0], skip_special_tokens=True)
    else:
        processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        inuts = processor(images=image, return_tensors="pt")

        output = model.generate(**inuts)
        return (processor.decode(output[0], skip_special_tokens=True))

    

if __name__ == '__main__':
    app.run(debug=True)
