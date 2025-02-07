
import librosa
import numpy as np

from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler


class EmotionRecognizer:
    def __init__(self, model_path="model/model.h5"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.required_time_steps = 352
        self.emotion_map = {
            0: "neutral",
            1: "happy",
            2: "sad",
            3: "angry",
            4: "fear",
            5: "disgust",
        }

    def load_model(self):
        """Load the trained model."""
        try:
            self.model = load_model(self.model_path)
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False

    def extract_features(self, audio_path):
        """Extract and normalize audio features."""
        try:
            y, sr = librosa.load(audio_path, sr=22050, duration=6)

            frame_length = 2048
            hop_length = 512

            zcr = librosa.feature.zero_crossing_rate(y, frame_length=frame_length, hop_length=hop_length)
            rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)

            min_time_steps = min(zcr.shape[1], rms.shape[1], mfccs.shape[1])
            zcr = zcr[:, :min_time_steps]
            rms = rms[:, :min_time_steps]
            mfccs = mfccs[:, :min_time_steps]

            features = np.vstack([zcr, rms, mfccs])

            if features.shape[1] < self.required_time_steps:
                repeat_times = self.required_time_steps // features.shape[1] + 1
                features = np.tile(features, (1, repeat_times))[:, : self.required_time_steps]
            elif features.shape[1] > self.required_time_steps:
                start_idx = (features.shape[1] - self.required_time_steps) // 2
                features = features[:, start_idx : start_idx + self.required_time_steps]

            features = features.T

            if self.scaler is None:
                self.scaler = StandardScaler()
                features_normalized = self.scaler.fit_transform(features)
            else:
                features_normalized = self.scaler.transform(features)

            return np.expand_dims(features_normalized, axis=0)

        except Exception as e:
            print(f"Error in feature extraction: {str(e)}")
            raise

    def predict_emotion(self, audio_path):
        """Predict emotion with probabilities."""
        try:
            if self.model is None:
                if not self.load_model():
                    return None, None, None

            X_input = self.extract_features(audio_path)
            predictions = self.model.predict(X_input, verbose=0)

            emotion_probabilities = {
                self.emotion_map[i]: float(prob) for i, prob in enumerate(predictions[0])
            }

            predicted_class = np.argmax(predictions[0])
            predicted_emotion = self.emotion_map[predicted_class]
            confidence = predictions[0][predicted_class]

            return predicted_emotion, confidence, emotion_probabilities

        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return None, None, None
