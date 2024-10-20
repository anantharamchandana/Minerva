from flask import Flask, request, jsonify
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch

app = Flask(__name__)

# Load the model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Get the audio file from the request
    audio_file = request.files['audio']
    inputs = processor(audio_file.read(), sampling_rate=16000, return_tensors="pt")
    
    # Generate transcription
    with torch.no_grad():
        predicted_ids = model.generate(**inputs)
    
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return jsonify({'transcription': transcription})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
