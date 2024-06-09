from flask import Flask, render_template, request
from flask_cors import CORS
import joblib
import numpy as np
import webbrowser
import threading
import os

app = Flask(__name__)
CORS(app)

# Load scaler
scaler = joblib.load('models/scaler.joblib')

# Load KMeans model
kmeans_model = joblib.load('models/model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy dữ liệu từ form
        Education = (request.form['Education'])
        Marital_Status = (request.form['Marital_Status'])
        Income = float(request.form['Income'])
        Wines = float(request.form['Wines'])
        Fruits = float(request.form['Fruits'])
        Meat = float(request.form['Meat'])
        Fish = float(request.form['Fish'])
        Sweet = float(request.form['Sweet'])
        Gold = float(request.form['Gold'])
        Age = int(request.form['Age'])
        Children = int(request.form['Children'])
        Expenses = int(request.form['Expenses'])

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

        # # Đề xuất sản phẩm dựa trên cụm
        # recommendations = {
        #     0: 'Wines, Fish, Gold',
        #     1: 'Wines, Fish, Gold',
        #     2: 'Wines, Fish, Gold',
        #     3: 'Wines, Fish, Gold',
        # }

        # recommendation = recommendations.get(cluster[0], 'Không có đề xuất')

        return render_template('index.html', cluster=cluster[0])

    except Exception as e:
        return str(e)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5500/')

if __name__ == '__main__':
    # Kiểm tra nếu ứng dụng không chạy ở chế độ debug thì mới mở trình duyệt
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.25, open_browser).start()
    app.run(debug=True, port=5500)
