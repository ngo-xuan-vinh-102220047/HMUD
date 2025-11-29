from PIL import Image
import requests
from io import BytesIO
import streamlit as st
import torchvision.transforms as transforms

# Load image from URL

def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        return img
    except Exception:
        return None

# Preprocessing

def get_transform(img_size=224):
    return transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
