# util/predict_analysis.py

import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np

def run_full_prediction(model, img, device, class_names, transform, topk=5):
    """
    Phân tích dự đoán đầy đủ: 
    - preprocess → model.eval → softmax
    - predicted class
    - top-k
    - probabilities array
    """

    input_tensor = transform(img).unsqueeze(0)
    model.eval()

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = F.softmax(outputs, dim=1).squeeze()

    prob_np = probabilities.cpu().numpy()
    top_p, top_idx = torch.topk(probabilities, topk)

    prediction = {
        "predicted_class": class_names[top_idx[0].item()],
        "confidence": float(top_p[0].item()),
        "all_probs": prob_np,
        "topk": [
            (class_names[top_idx[i].item()], float(top_p[i].item()))
            for i in range(topk)
        ]
    }
    return prediction
