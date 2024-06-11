from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import webbrowser
import threading
import os
import json

app = Flask(__name__)
CORS(app)

# Load scaler
scaler = joblib.load('models/scaler.joblib')

# Load KMeans model
kmeans_model = joblib.load('models/model.joblib')

# Load cluster information from JSON file
with open('models/cluster.json', 'r', encoding='utf-8') as file:
    cluster_data = json.load(file)

@app.route('/')
def home():
    return render_template('index.html', cluster_infor=cluster_data.get("undenfined"))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy dữ liệu từ form
        data = request.json
        Education = data['Education']
        Marital_Status = data['Marital_Status']
        Income = float(data['Income'])
        Wines = float(data['Wines'])
        Fruits = float(data['Fruits'])
        Meat = float(data['Meat'])
        Fish = float(data['Fish'])
        Sweet = float(data['Sweet'])
        Gold = float(data['Gold'])
        Age = int(data['Age'])
        Children = int(data['Children'])
        Expenses = int(data['Expenses'])

        # Chuyển dữ liệu về dạng chuẩn
        education_map = {
            'Graduation': 1,
            'PhD': 2,
            'Master': 3,
            'Basic': 0
        }
        marial_status_map = {
            'In relationship': 1, 
            'Single': 0
        }
        Education = int(education_map.get(Education))
        Marital_Status = int(marial_status_map.get(Marital_Status))
        
        # Tạo DataFrame từ dữ liệu nhập vào
        data = np.array([[Education, Marital_Status, Income, Wines, Fruits, Meat, Fish, Sweet, Gold, Age, Children, Expenses]])

        # Chuẩn hóa dữ liệu
        # scaled_data = scaler.transform(data)

        # Dự đoán nhóm phân cụm cho dữ liệu
        cluster = kmeans_model.predict(data)

        # Lấy thông tin cụm
        cluster_infor = cluster_data.get(str(cluster[0]), cluster_data.get("undenfined"))

        # Convert numpy integer to Python int
        result = {
            "cluster": int(cluster[0]),
            "cluster_infor": cluster_infor
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5500/')

if __name__ == '__main__':
    # Kiểm tra nếu ứng dụng không chạy ở chế độ debug thì mới mở trình duyệt
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.25, open_browser).start()
    app.run(debug=True, port=5500)
