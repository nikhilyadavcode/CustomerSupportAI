import joblib

# Load trained model
model = joblib.load("intent_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


def detect_intent(message: str):

    X = vectorizer.transform([message])

    prediction = model.predict(X)

    return prediction[0]