from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
