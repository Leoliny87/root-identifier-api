from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

# 初始化模型（Vercel冷启动时会加载）
model = None

def load_model():
    global model
    model_path = os.path.join(os.path.dirname(__file__), '../model/root_type_recognition_model.h5')
    model = tf.keras.models.load_model(model_path)

@app.route('/api/predict', methods=['POST'])
def predict():
    global model
    
    # 确保模型已加载
    if model is None:
        load_model()
    
    # 处理图片上传
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    try:
        # 图像预处理
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img = img.resize((180, 180))
        arr = np.array(img).astype(np.float32) / 255.0
        input_data = np.expand_dims(arr, axis=0)
        
        # 预测
        prediction = model.predict(input_data)
        result = "直根系" if prediction[0][0] < 0.5 else "须根系"
        
        return jsonify({"result": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
