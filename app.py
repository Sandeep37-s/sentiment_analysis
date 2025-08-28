# app.py (Updated)
from flask import Flask, render_template, request
import pickle
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# --- Initialize Flask App ---
app = Flask(__name__)

# --- Download NLTK data if not already present ---
try:
    stopwords.words('english')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)

# --- Load the Vectorizer and Model ---
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('sentiment_model.pkl', 'rb') as f:
    model = pickle.load(f)

# --- Preprocessing Function ---
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+|\@\w+|\#', '', text, flags=re.MULTILINE)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return " ".join(lemmatized_tokens)

# --- Define Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    # This is the new route for our about page
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_text = request.form['text']
        cleaned_text = preprocess_text(user_text)
        vectorized_text = vectorizer.transform([cleaned_text])
        prediction = model.predict(vectorized_text)[0]
        label_map = {0: "negative", 4: "positive"}
        prediction_text = label_map.get(prediction, "unknown")
        return render_template('index.html', prediction=prediction_text, original_text=user_text)
    except Exception as e:
        return render_template('index.html', prediction="unknown", original_text=user_text)


# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)