📝 Sentiment Analysis Web App

A Machine Learning & Deep Learning powered web application that predicts the sentiment (Positive, Negative, Neutral) of user input text.
The project uses text preprocessing, ML models (Logistic Regression, Naive Bayes, etc.), and a simple Flask web interface to provide real-time sentiment predictions.

🚀 Features

🔹 User-Friendly Web App built with Flask

🔹 Text Preprocessing: stopword removal, punctuation cleaning, HTML tag removal, URL removal, spelling correction, etc.

🔹 Multiple ML Models trained (Logistic Regression, Naive Bayes, SVM, etc.)

🔹 Hybrid/Ensemble Approach for better accuracy

🔹 Admin Panel (Optional): View stored predictions & user inputs (if DB connected)

🔹 Real-Time Prediction of sentiment

🛠️ Tech Stack

Programming Language: Python

Machine Learning: scikit-learn, nltk, transformers (optional for BERT)

Web Framework: Flask

Frontend: HTML, CSS (Tailwind for styling)

📊 Model Training

Preprocessing includes:
✅ Removing stopwords
✅ Removing HTML tags
✅ Removing punctuation
✅ Removing URLs
✅ Spelling correction
✅ Tokenization + Vectorization (TF-IDF)

Models Used:

Logistic Regression

Multinomial Naive Bayes

Support Vector Machine (SVM)

Hybrid Ensemble Model

Evaluation Metrics:

Accuracy

Precision, Recall, F1-score

Confusion Matrix

📂 Project Structure
sentiment-analysis/
│── app.py              # Flask application  
│── templates/          # HTML files  
│── static/             # CSS/JS files  
│── models/             # Saved ML/DL models  
│── preprocessing.py    # Text cleaning functions  
│── requirements.txt    # Required Python packages  
│── README.md           # Project documentation  

⚡ How to Run Locally

Clone the repository:

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>


Create & activate virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate      # for Windows  
source venv/bin/activate   # for Linux/Mac


Install dependencies:

pip install -r requirements.txt


Run the Flask app:

python app.py


Open in browser:

http://127.0.0.1:5000/

🎯 Future Improvements

Deploy the app on Heroku / Render / AWS

Add Deep Learning (LSTM / BERT) for better accuracy

Build a mobile app version of the web app

Add visualizations (word clouds, sentiment distribution graphs)

📌 Author

👤 Sandeep Kumar
