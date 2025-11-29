import streamlit as st
from PIL import Image
from util.utilities import load_image_from_url

# ========================
# INPUT HANDLING MODULE
# ========================

def get_input_image():
    """
    Xử lý 3 loại đầu vào: Upload, URL, Camera
    Trả về ảnh PIL hoặc None
    """
    option = st.radio("Chọn nguồn ảnh", [
        "Upload từ máy",
        "Ảnh từ URL",
        "Camera thời gian thực (ảnh)"
    ])

    image = None

    # Upload từ thiết bị
    if option == "Upload từ máy":
        file = st.file_uploader("Tải ảnh", type=["jpg", "png", "jpeg"])
        if file:
            image = Image.open(file).convert("RGB")

    # URL
    elif option == "Ảnh từ URL":
        url = st.text_input("Nhập URL ảnh:")
        if url:
            img = load_image_from_url(url)
            if img:
                image = img
            else:
                st.error("Không tải được ảnh từ URL!")

    # Camera
    elif option == "Camera thời gian thực (ảnh)":
        cam = st.camera_input("Chụp ảnh")
        if cam:
            image = Image.open(cam).convert("RGB")

    return image