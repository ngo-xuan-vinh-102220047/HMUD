import streamlit as st

import torch
from PIL import Image
import cv2
import numpy as np

from model.model_load import load_checkpoint
from util.utilities import get_transform
from util.inference import predict_image, predict_image_probs
from util.recycle_info import get_recycle_info
from util.chart_render import display_prediction_charts
from util.predict_analysis import run_full_prediction
from components.upload import get_input_image
from components.result_display import class_probs_to_base64_image
from components.result_display import show_topk_predictions, show_topk_chart

# ========================
# 
# ========================

st.set_page_config(
    page_title="Garbage Classification Web App",
    page_icon="♻️",
    layout="centered",
)

# ========================
# CONFIG
# ========================
MODEL_PATH = "model/garbage_classifier_model.pth"
CLASS_NAMES = [
    'battery', 
    'biological', 
    'cardboard', 
    'clothes',
    'glass', 
    'metal', 
    'paper', 
    'plastic', 
    'shoes', 
    'trash'
]
IMG_SIZE = 224

st.title("♻️ Garbage Classification Web App")
st.write("Upload ảnh, nhập URL hoặc dùng camera để phân loại rác!")

# Load Model
@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_checkpoint(MODEL_PATH, device, num_classes=len(CLASS_NAMES))
    return model, device

model, device = load_model()

# ========================
# INPUT OPTIONS
# ========================

image = get_input_image()

# ========================
# INFERENCE
# ========================
if image:
    st.image(image, caption="Ảnh đầu vào", use_column_width=True)

    # Sử dụng pipeline phân tích đầy đủ: transform + model.eval + softmax + top-k
    transform = get_transform(IMG_SIZE)
    prediction = run_full_prediction(model, image, device, CLASS_NAMES, transform, topk=5)

    # all_probs có thể là numpy array -> chuyển thành list float
    all_probs = (prediction["all_probs"].tolist()
                 if hasattr(prediction["all_probs"], "tolist")
                 else list(prediction["all_probs"]))

    # Hiển thị biểu đồ xác suất (sử dụng toàn bộ vector probs)
    img_data_uri = class_probs_to_base64_image(all_probs, CLASS_NAMES)
    st.image(img_data_uri, caption="Xác suất dự đoán", use_column_width=True)

    # Kết quả chính
    st.subheader(f"Kết quả: {prediction['predicted_class']}")
    st.write(f"Độ tin cậy: {prediction['confidence']*100:.2f}%")

    show_topk_chart(prediction["topk"])
    # st.image(img_data_uri, caption="Top 5 dự đoán", use_column_width=True)

    # Hiển thị top-k chi tiết (hàm show_topk_predictions đã được import)
    try:
        show_topk_predictions(prediction["topk"])
    except Exception:
        # Fallback: in ra text nếu component không hợp lệ
        st.write("Top-K predictions:")
        for cls, p in prediction["topk"]:
            st.write(f"- {cls}: {p*100:.2f}%")

    # Hiển thị thông tin tái chế
    status, note = get_recycle_info(prediction['predicted_class'])
    if status == 'Tái chế được':
        st.success(f"Có thể tái chế — {note}")
    elif status == 'Tái chế đặc biệt':
        st.warning(f"Yêu cầu xử lý đặc biệt — {note}")
    elif status == 'Không tái chế':
        st.error(f"Không tái chế — {note}")
    else:
        st.info(f"{status} — {note}")
