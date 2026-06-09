from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load("data/churn_model_clean.pkl")

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = float(request.form['Age'])
        account_manager = int(request.form['Account_Manager'])
        years = float(request.form['Years'])
        num_sites = float(request.form['Num_Sites'])

        data = pd.DataFrame([{
            'Age': age,
            'Account_Manager': account_manager,
            'Years': years,
            'Num_Sites': num_sites
        }])

        prediction = int(model.predict(data)[0])

        return jsonify({
            "prediction": prediction,
            "message": "Churn" if prediction == 1 else "No Churn"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)