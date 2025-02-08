# HearToHelp

### 🌟 Predict Mental State Using Voice Analysis

HearToHelp is an AI-powered web application that analyzes human speech to predict mental states using deep learning techniques. Our project leverages **Machine Learning & Audio Processing** to detect emotions and mental well-being based on voice input.

## 🚀 Features

- 🎙️ **Audio-Based Mental State Prediction**  
- 🧠 **Deep Learning with TensorFlow & Keras**  
- 🎵 **Feature Extraction with Librosa**  
- 🌐 **Web Interface Built with Flask, Bootstrap & Vanilla CSS**  
- 📊 **Real-Time Predictions & Visualization**  

## 🛠️ Tech Stack

### 🔹 Backend  
- **Flask** - Lightweight Python web framework  
- **TensorFlow & Keras** - Model training & inference  
- **Librosa** - Audio processing & feature extraction  

### 🔹 Frontend  
- **Bootstrap** - Styling & UI components  
- **Vanilla CSS** - Custom styles  

### 🔹 Database  
- currently we have not integrated any database

## 📌 Installation

1️⃣ **Clone the repository**  
```sh
git clone https://github.com/MohammadAdnanKhan/HearToHelp_
cd HearToHelp_
```

2️⃣ **Create a virtual environment (Optional but recommended)**
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3️⃣ **Install dependencies**
```sh
pip install -r requirements.txt
```

4️⃣ **Run the Flask app**
```sh
python app.py
```
The app will be available at: **http://127.0.0.1:5000/**

## 🏗️ How It Works  

1. The user uploads an **audio file** (speech recording).  
2. **Librosa** extracts key audio features (MFCC, Mel spectrogram, etc.).  
3. Our **deep learning model** (CNN/LSTM) predicts the speaker’s **emotional state**.  
4. The result is displayed on the **web app**.  

## 📅 Future Plans  
- 🌍 Deploy on cloud (AWS, Heroku, Render, etc.)  
- 📱 Develop a mobile app  
- 🎭 Improve emotion classification accuracy  

## 🤝 Contributing  
We welcome contributions! Feel free to open an **issue** or **pull request**.  

## 📜 License  
This project is **MIT Licensed**.  

---

### 🚀 Team HearToHelp  
👨‍💻 **Team Members:**  
- [Mohd Adnan Khan]()
- [Mohd Shamoon]()
- [Muhammed Ashrah]()
- [Mohd Reyyan]()

---