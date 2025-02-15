import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import warnings
from emotion_recognizer import EmotionRecognizer
from flask_cors import CORS
from id_generator import generate_random_string
import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request
from dotenv import load_dotenv
load_dotenv()
from functools import wraps

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000"])
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_database.db'   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# users model
class User(db.Model):
    id = db.Column(db.String(16), primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
        return f'{{"id": "{self.id}", "username": "{self.username}", "email": "{self.email}", "password_hash": "{self.password_hash}"}}'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(16), db.ForeignKey('user.id'), nullable=False)
    emotion = db.Column(db.String(16), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    probabilities = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'{{"id": "{self.id}", "user_id": "{self.user_id}", "emotion": "{self.emotion}", "confidence": "{self.confidence}", "probabilities": "{self.probabilities}"}}'

# Create the tables
with app.app_context():
    # db.drop_all()
    # print("Dropped all tables")
    db.create_all()
    print("Database and tables created")


app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

def jwt_middleware():
    """ Custom middleware to enforce JWT authentication """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()  # Checks if request contains a valid JWT
            except Exception:
                return jsonify({"error": "Unauthorized"}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator

recognizer = EmotionRecognizer("model/model.h5")

# API to serve Static files
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/auth")
def auth():
    return render_template('auth.html')

@app.route("/signup", methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"message": "Please provide all the required fields"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists, please login"}), 400

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    new_user = User(id=generate_random_string(), username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful, login to continue"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Please provide all the required fields"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found, please signup first"}), 404
    
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if user.password_hash != hashed_password:
        return jsonify({"message": "Invalid password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"message":"Login successful", "access_token": access_token, "username": user.username})

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
@jwt_middleware()
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
        # return jsonify({"error": str(e)}), 500
        return jsonify({"error": "Failed to predict emotion"}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
