import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import warnings
from emotion_recognizer import EmotionRecognizer

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


recognizer = EmotionRecognizer("model/model.h5")

# API to serve Static files
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/detection")
def detection():
    return render_template('detection.html')

@app.route("/resources")
def resources():
    return render_template('resources.html')

@app.route("/community")
def community():
    return render_template('community.html')

@app.route("/meditation")
def meditation():
    return render_template('meditation.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/educational-resources")
def educational_resources():
    return render_template('educational-resources.html')

@app.route("/spiritual-resources")
def spiritual_resources():
    return render_template('spiritual-resources.html')

@app.route("/counsellors")
def counsellors():
    return render_template('counsellors.html')

@app.route("/emergency-contacts")
def emergency_contacts():
    return render_template('emergency-contacts.html')

@app.route("/terms")
def terms():
    return render_template('terms.html')

# API route to detect emotion
@app.route('/api/detect', methods=['POST'])
def detect_emotion():
    """API endpoint to receive an audio file and return emotion prediction."""
    if 'audio' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file temporarily
    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    audio_file.save(file_path)

    # Process audio file
    try:
        predicted_emotion, confidence, emotion_probabilities = recognizer.predict_emotion(file_path)
        os.remove(file_path)  # Clean up temp file

        if predicted_emotion is None:
            return jsonify({"error": "Failed to predict emotion"}), 500

        # Convert NumPy types to standard Python types
        confidence = float(confidence)  # Ensure it's a standard float
        emotion_probabilities = {key: float(value) for key, value in emotion_probabilities.items()}  # Convert dict values

        return jsonify({
            "emotion": predicted_emotion,
            "confidence": confidence,
            "probabilities": emotion_probabilities
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000, debug=False)
